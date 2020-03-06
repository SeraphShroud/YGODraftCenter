from service.ygo_card_db_service import YGOCardDBService

class InvalidCreationError(Exception):
    """Exception Raised when Game move is not Allowed
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class InvalidMoveError(Exception):
    """Exception Raised when Game move is not Allowed
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class DraftService:
    def __init__(self, max_players : int, main_deck_list : list, extra_deck_list : list, time_limit : int, pack_size : int):
        if max_players < 2:
            raise InvalidCreationError("Not enough players")
        main_deck_length = len(main_deck_list)
        extra_deck_length = len(extra_deck_list)
        if main_deck_length % pack_size > 0:
            raise InvalidCreationError("Main deck cannot be split into pack size evenly")
        if extra_deck_length % pack_size > 0:
            raise InvalidCreationError("Extra deck cannot be split into pack size evenly")
        if (main_deck_length / pack_size) % max_players > 0:
            raise InvalidCreationError("not enough main packs for players")
        if (extra_deck_length / pack_size) % max_players > 0:
            raise InvalidCreationError("not enough main packs for players")
        self.players = range(0, max_players)
        self.players_deck = {}
        if pack_size < 1:
            raise InvalidCreationError("pack size is too small")
        self.pack_size = pack_size
        if time_limit < 1:
            raise InvalidCreationError("time limit is too small")
        self.time_limit = time_limit