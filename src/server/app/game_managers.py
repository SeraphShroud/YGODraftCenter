from app.game_exceptions import InvalidGameError, TooManyPlayersGameError
from models.draft_params import DraftParams
from service.draft_service import DraftService, InvalidMoveError
from enums.strings import Draft, YGODraft


class GameManager(object):
    def __init__(self):
        """Records All Games in a Dictionary and create a sequence of game ids
        """
        self.games = {}
        self.max_game_id = 100
        self.players = {}
        self.max_players = 3
        self.draft_params = {}
        self.max_draft_params_id = 100

    def _get_next_game_id(self):
        """Returns next game id
        """
        if self.max_game_id > 100000:
            self.max_game_id = 100
        self.max_game_id += 1
        return self.max_game_id

    def _get_next_draft_param_id(self):
        """Returns next draft param id
        """
        if self.max_draft_params_id > 100000:
            self.max_draft_params_id = 100
        self.max_draft_params_id += 1
        return self.max_draft_params_id

    def new_game(self, handler):
        """Creates a new Game and returns the game id
        """
        game_id = self._get_next_game_id()
        self.games[game_id] = {0: handler}
        self.players[game_id] = [0]
        return game_id

    def new_draft_param(self):
        """Creates a new draft parameters and returns the prameter id
        """
        draft_param_id = self._get_next_draft_param_id()
        self.draft_params[draft_param_id] = DraftParams()
        return draft_param_id

    def set_draft_params(self, num_players, round_time, pack_size, param_id):
        draft_param = self.draft_params[param_id]
        draft_param.setPlayerLength(num_players)
        draft_param.setRoundTime(round_time)
        draft_param.setPackSize(pack_size)

    def set_draft_decks(self, main_list, extra_list, param_id):
        draft_param = self.draft_params[param_id]
        draft_param.setMainList(main_list)
        draft_param.setExtraList(extra_list)

    def get_draft_param(self, param_id):
        return self.draft_params[param_id]

    def join_game(self, game_id, handler):
        """Returns player_id if join is successful.
        Raises InvalidGame when it could not join the game
        """
        game = self.get_game(game_id)
        player_id = self.new_player(game_id)
        if game.get(player_id) is None:
            game[player_id] = handler
            return player_id
        # Game ID not found.
        raise InvalidGameError

    def end_game(self, game_id):
        """Removes the Game from the games registry
        """
        if game_id in self.games:
            del self.games[game_id]
            del self.players[game_id]

    def get_pair(self, game_id, handler):
        """Returns the paired Handler
        """
        game = self.get_game(game_id)
        if handler == game.get("handler_a"):
            return game.get("handler_b")
        elif handler == game.get("handler_b"):
            return game.get("handler_a")
        else:
            raise InvalidGameError
    
    def get_game(self, game_id):
        """Returns the game instance.  Raises Error when game not found
        """
        game = self.games.get(game_id)
        if game:
            return game
        raise InvalidGameError

    def get_players(self, game_id):
        """Returns the player id for a game.  Raises Error when player not found
        """
        players = self.players.get[game_id]
        if players:
            return players
        raise InvalidGameError

    def new_player(self, game_id):
        """creates a new player for a game 
        """
        players = self.players[game_id]
        if len(players) >= self.max_players or len(players) == 0:
            raise TooManyPlayersGameError

        players.append(players[-1] + 1)
        return players[-1]

    def get_other_players(self, game_id, handler):
        """Returns the paired Handler
        """
        game = self.get_game(game_id)
        other_players = []
        for player, player_handler in game.items():
            if handler != player_handler and isinstance(player, int):
                other_players.append(player_handler)

        return other_players


class DraftGameManager(GameManager):
    """Extends Game Manager to add methods specific to Draft Game
    """

    def new_game(self, handler, param_id):
        """Extend new_game with tic_tac_toe instance.
        """
        game_id = super().new_game(handler)
        draft_param = super().get_draft_param(param_id)
        game = self.get_game(game_id)
        # game["tic_tac_toe"] = TicTacToe()
        game[YGODraft.GAME] = DraftService(draft_param)
        game[YGODraft.GAME].createDraft()
        game[YGODraft.PARAM] = draft_param
        game[YGODraft.ROUND] = 0
        return game_id

    def all_players_joined(self, game_id, player_id):
        game = self.get_game(game_id)
        draft_param = game[YGODraft.PARAM]
        if player_id == draft_param.getPlayerLength() - 1:
            return True
        else:
            return False

    def record_move(self, game_id, selection, player_id):
        """Record the move onto tic_tac_toe instance
        """
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        try:
            game[YGODraft.GAME].pick_m_card(player_id, round, selection)
        except InvalidMoveError:
            raise InvalidGameError
    
    def abort_game(self, game_id):
        """Aborts the game
        """
        game = self.get_game(game_id)
        tic_tac_toe = game["tic_tac_toe"]
        tic_tac_toe.abort_game()

    def has_game_ended(self, game_id):
        """Returns True if the game has ended.
        Game cound end because of them won or it's a draw or no more open positions.
        """
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        ygo_draft = game[YGODraft.GAME]
        if ygo_draft.has_ended(round):
            return True
        return False

    def get_game_result(self, game_id, handler):
        """Returns game result with a "W", "L", "D" or "E"
        """
        game = self.get_game(game_id)
        if not game.get("result"):
            # Compute game result
            self.has_game_ended(game_id)

        if game["result"] == "D" or game["result"] == "E":
            return game["result"]
        elif (game["result"] == "A" and game["handler_a"] == handler) or \
                (game["result"] == "B" and game["handler_b"] == handler):
            return "W"
        elif game["result"]:
            return "L"
        else:
            return ""  # Game is still ON.

    def has_round_ended(self, game_id):
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        if not game[YGODraft.GAME].has_all_players_picked():
            return False
        if len(game[YGODraft.GAME].get_m_pack(0, round)) > 0:
            return False
        return True

    def update_round(self, game_id):
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        game[YGODraft.ROUND] = round + 1

    def has_all_players_picked(self, game_id):
        game = self.get_game(game_id)
        if not game[YGODraft.GAME].has_all_players_picked():
            return False
        return True

    def rotate_pack(self, game_id):
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        if round % 2:
            game[YGODraft.GAME].rotate_pack(round, "left")
        else:
            game[YGODraft.GAME].rotate_pack(round, "right")

    def get_pack(self, game_id, player_id):
        game = self.get_game(game_id)
        round = game[YGODraft.ROUND]
        return game[YGODraft.GAME].get_m_pack(player_id, round)

    def get_deck(self, game_id, player_id):
        game = self.get_game(game_id)
        ygo_draft = game[YGODraft.GAME]
        return ygo_draft.get_deck(player_id)
