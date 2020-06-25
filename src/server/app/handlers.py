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
from enums.strings import MongoDB

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
    """Render Game page
    """

    def get(self):
        self.render("../client/login.html")


class UploadHandler(BaseHandler):
    def post(self):
        ydk_file = self.request.files['file'][0]
        deck_name, id_list = self.parse_ydk(ydk_file)
        print(f"Deck name: {deck_name}\nID List: {id_list}")
        card_service = YGOCardDBService(MongoDB.DB_NAME, MongoDB.CARD_COLLECTION_NAME, MongoDB.DB_URL)
        # Currently only allows for UNIQUE id's, so need to figure out how to allow multiples of a card
        card_info = card_service.get_card_list(id_list)
        self.finish({
            'deck_name': deck_name,
            'id_list': id_list,
            'card_info_list': card_info
        })

    def parse_ydk(self, ydk: dict, singleton=True) -> tuple:
        # Need to validate the contents of the ydk to ensure it's the correct file type
        deck_name = ydk.get('filename')
        content_list = ydk.get('body').decode("utf-8").splitlines()
        id_list = [int(card_id) for card_id in content_list if card_id[0].isdigit()]
        return (deck_name, id_list)


class DraftSocketHandler(WebSocketHandler):

    def initialize(self, game_manager, *args, **kwargs):
        """Initialize game parameters.  Use Game Manager to register game
        """
        self.game_manager = game_manager
        self.game_id = None
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
                self.game_manager.record_move(self.game_id, player_move, self)
            self.send_message(action="opp-move")
            self.send_pair_message(action="move", opp_move=player_selection)

            # Check if the game is still ON
            if self.game_manager.has_game_ended(self.game_id):
                game_result = self.game_manager.get_game_result(
                    self.game_id, self)
                self.send_message(action="end", result=game_result)
                opp_result = "L" if game_result == "W" else game_result
                self.send_pair_message(action="end", result=opp_result)
                self.game_manager.end_game(self.game_id)

        elif action == "join":
            # Get the game id
            try:
                game_id = int(data.get("game_id"))
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
                # Tell both players that they have been paired, so reset the pieces
                self.send_message(action="joined", game_id=game_id, player_id=player_id)
                self.send_pair_message(action="paired", game_id=game_id, player_id=player_id)
                # One to wait, other to move
                if self.game_manager.all_players_joined(game_id, player_id):
                    self.send_message(action="game-start")
                    self.send_pair_message(action="game-start")

        elif action == "new":
            # Create a new game id and respond the game id
            self.game_id = self.game_manager.new_game(self)
            self.send_message(action="wait-pair", game_id=self.game_id, player_id=0)

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
