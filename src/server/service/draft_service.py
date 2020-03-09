import random
from model.draft_params import DraftParams


class InvalidMoveError(Exception):
    """Exception Raised when Game move is not Allowed
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DraftService:
    def __init__(self, draft_params: DraftParams):
        self.max_players = draft_params.getPlayerLength()
        self.main_deck_list = draft_params.getMainList()
        self.extra_deck_list = draft_params.getExtraList()
        self.pack_size = draft_params.getPackSize()
        self.time_limit = draft_params.getTimeLimit()
        self.player_decks = {}
        self.player_e_decks = {}

    def createDraft(self):
        random.shuffle(self.main_deck_list)
        self.player_m_decks = {}
        deck_i = 0
        pack_i = self.pack_size
        for i in range(1, self.max_players):
            self.player_m_decks[i] = self.main_deck_list[deck_i, pack_i]
            deck_i += pack_i
            pack_i += self.pack_size
