"""
Request Handlers
"""
from builtins import super
import logging
import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from app.game_exceptions import InvalidGameError, TooManyPlayersGameError
from service.ygo_card_db_service import YGOCardDBService
from enums.strings import Draft
from app.game_managers import DraftGameManager

logger = logging.getLogger()


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        logger.debug("Setting CORS headers")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers",
                        "access-control-allow-origin, authorization, content-type")

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class IndexHandler(BaseHandler):
    """Redirect to Tic-Tac-Toe
    """

    def get(self):
        self.redirect('/ygoserver')


class DraftHandler(BaseHandler):
    def initialize(self, game_manager: DraftGameManager, card_service: YGOCardDBService, *args, **kwargs):
        """Initialize game parameters.  Use Game Manager to register game
        """
        self.game_manager = game_manager
        super().initialize(*args, **kwargs)
        self.card_service = card_service

    def get(self):
        current_games = self.game_manager.get_all_games()
        self.finish({
            'current_games': current_games
        })

    def post(self):
        ydk_file = self.request.files['file'][0]
        num_players = int(self.request.body_arguments['num_players'][0])
        round_time = int(self.request.body_arguments['round_time'][0])
        pack_size = int(self.request.body_arguments['pack_size'][0])
        deck_name, main_list, extra_list = self.parse_ydk(ydk_file)
        id_list = main_list + extra_list
        print(f"Deck name: {deck_name}\nID List: {id_list}")
        # Currently only allows for UNIQUE id's, so need to figure out how to allow multiples of a card
        card_info = self.card_service.get_card_list(id_list)
        draft_param_id = self.game_manager.new_draft_param()
        self.game_manager.set_draft_params(num_players, round_time, pack_size, draft_param_id)
        self.game_manager.set_draft_decks(main_list, extra_list, draft_param_id)
        self.finish({
            'draft_param_id': draft_param_id,
            'deck_name': deck_name,
            'id_list': id_list,
            'card_info_list': card_info
        })

    def parse_ydk(self, ydk: dict, singleton=True) -> tuple:
        # Need to validate the contents of the ydk to ensure it's the correct file type
        deck_name = ydk.get('filename')
        content_list = ydk.get('body').decode("utf-8").splitlines()
        main_list = []
        extra_list = []
        id_list = main_list
        for card_id in content_list:
            if isinstance(card_id, str) and card_id == Draft.EXTRA:
                id_list = extra_list
            if card_id[0].isdigit():
                id_list.append(int(card_id))
        return (deck_name, main_list, extra_list)


class DraftSocketHandler(WebSocketHandler):
    # to only be used during testing must remove when running on production
    def check_origin(self, origin):
        return True

    def initialize(self, game_manager: DraftGameManager, card_service: YGOCardDBService, *args, **kwargs):
        """Initialize game parameters.  Use Game Manager to register game
        """
        self.game_manager = game_manager
        self.card_service = card_service
        self.game_id = None
        self.player_id = None
        self.player_name = None
        super().initialize(*args, **kwargs)

    def open(self):
        """Opens a Socket Connection to client
        """
        self.send_message(action="open", message="Connected to Game Server")

    def on_message(self, message):
        """Respond to messages from connected client.
        Messages are of form -
        {
            action: <action>,
            <data>
        }
        Valid Actions: new, join, abort, move.
        new - Request for new game
        join - Join an existing game (but that's not been paired)
        abort - Abort the game currently on
        move - Record a move
        """
        data = json.loads(message)
        action = data.get("action", "")
        if action == "move":
            # Game is going on
            # Set turn to False and send message to opponent
            player_selection = data.get("card_id")
            player_move = int(player_selection)
            if player_move:
                try:
                    self.game_manager.record_move(self.game_id, player_move, self.player_id)
                except InvalidGameError:
                    self.send_message(action="invalid-move", message="card is not in players pack")
                else:
                    self.send_message(action="move", selection=player_selection)
                    self.send_pair_message(action="opp-move", player_id=self.player_id, player_name=self.player_name)

            # Check if the game is still ON
            if self.game_manager.has_game_ended(self.game_id):
                self.send_card_info("get-deck", Draft.DECK)
                self.send_pair_card_info("get-deck", Draft.DECK)
                self.game_manager.end_game(self.game_id)
            if self.game_manager.has_round_ended(self.game_id):
                self.game_manager.update_round(self.game_id)
                self.send_card_info(action="get-pack", card_list=Draft.PACK)
                self.send_pair_card_info(action="get-pack", card_list=Draft.PACK)
            if self.game_manager.has_all_players_picked(self.game_id):
                self.game_manager.rotate_pack(self.game_id)
                self.send_card_info(action="get-pack", card_list=Draft.PACK)
                self.send_pair_card_info(action="get-pack", card_list=Draft.PACK)

        elif action == "join":
            # Get the game id
            try:
                game_id = int(data.get("game_id"))
                player_name = data.get("player_name")
                player_id = self.game_manager.join_game(game_id, self)
            except TooManyPlayersGameError:
                self.send_message(action="error", message="Max Players Met For Game Id: {}".format(
                    data.get("game_id")))
            except (ValueError, TypeError, InvalidGameError):
                self.send_message(
                    action="error", message="Invalid Game Id: {}".format(data.get("game_id")))
            else:
                # Joined the game.
                self.game_id = game_id
                self.player_id = player_id
                self.player_name = player_name
                # Tell both players that they have been paired, so reset the pieces
                other_player = self.game_manager.get_other_players(game_id, self)
                player_list = [player_name]
                for player in other_player:
                    player_list.append(player.player_name)
                self.send_message(action="joined", game_id=game_id, player_id=player_id, joined_player=player_name, players=player_list)
                self.send_pair_message(action="paired", game_id=game_id, player_id=player_id, joined_player=player_name, players=player_list)
                # One to wait, other to move
                if self.game_manager.all_players_joined(game_id, player_id):
                    self.send_message(action="game-start")
                    self.send_pair_message(action="game-start")
                    self.send_card_info(action="get-pack", card_list=Draft.PACK)
                    self.send_pair_card_info(action="get-pack", card_list=Draft.PACK)

        elif action == "new":
            # Create a new game id and respond the game id
            draft_param_id = int(data.get("draft_param_id"))
            player_name = data.get("player_name")
            game_name = data.get("game_name")
            self.player_name = player_name
            self.game_id = self.game_manager.new_game(self, draft_param_id, game_name)
            self.player_id = 0
            self.send_message(action="wait-pair", game_id=self.game_id, player_id=self.player_id, players=[player_name])

        elif action == "abort":
            self.game_manager.abort_game(self.game_id)
            self.send_message(action="end", game_id=self.game_id, result="A")
            self.send_pair_message(
                action="end", game_id=self.game_id, result="A")
            self.game_manager.end_game(self.game_id)

        else:
            self.send_message(
                action="error", message="Unknown Action: {}".format(action))

    def on_close(self):
        """Overwrites WebSocketHandler.close.
        Close Game, send message to Paired client that game has ended
        """
        self.send_pair_message(action="end", game_id=self.game_id, result="A")
        self.game_manager.end_game(self.game_id)

    def send_pair_message(self, action, **data):
        """Send Message to paired Handler
        """
        if not self.game_id:
            return
        try:
            player_handlers = self.game_manager.get_other_players(self.game_id, self)
        except InvalidGameError:
            logging.error(
                "Invalid Game: {0}. Cannot send pair msg: {1}".format(self.game_id, data))
        except TooManyPlayersGameError:
            logging.error(
                "Max Players: {0}. Cannot send pair msg: {1}".format(self.game_id, data))
        else:
            if player_handlers:
                for player_handler in player_handlers:
                    player_handler.send_message(action, **data)

    def send_message(self, action, **data):
        """Sends the message to the connected client
        """
        message = {
            "action": action,
            "data": data
        }
        try:
            self.write_message(json.dumps(message))
        except WebSocketClosedError:
            logger.warning(
                "WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            self.send_pair_message(action="pair-closed")
            self.close()
    
    def send_card_info(self, action, card_list):
        id_list = []
        if card_list == Draft.PACK:
            id_list = self.game_manager.get_pack(self.game_id, self.player_id)
        elif card_list == Draft.DECK:
            id_list = self.game_manager.get_deck(self.game_id, self.player_id)
        card_info = self.card_service.get_card_list(id_list)
        data = {}
        data["card_info_list"] = card_info
        message = {
            "action": action,
            "data": data
        }
        try:
            self.write_message(json.dumps(message))
        except WebSocketClosedError:
            logger.warning(
                "WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            self.send_pair_message(action="pair-closed")
            self.close()

    def send_pair_card_info(self, action, card_list):
        """Send Message to paired Handler
        """
        if not self.game_id:
            return
        try:
            player_handlers = self.game_manager.get_other_players(self.game_id, self)
        except InvalidGameError:
            logging.error(
                "Invalid Game: {0}. Cannot send pair pack info".format(self.game_id))
        except TooManyPlayersGameError:
            logging.error(
                "Max Players: {0}. Cannot send pair pack info".format(self.game_id))
        else:
            if player_handlers:
                for player_handler in player_handlers:
                    player_handler.send_card_info(action, card_list)
