import random
from server.models.draft_params import DraftParams


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
        self.time_limit = draft_params.getRoundTime()
        self.player_decks = {}
        self.player_e_decks = {}
        self.player_m_packs = {}
        self.player_e_packs = {}

    def createDraft(self):
        random.shuffle(self.main_deck_list)
        random.shuffle(self.extra_deck_list)
        deck_i = 0
        pack_i = self.pack_size
        num_packs = len(self.main_deck_list) / (self.pack_size * self.max_players)
        for round in range(0, num_packs):
            self.player_m_packs[round] = {round: []}
            for i in range(0, self.max_players):
                self.player_m_packs[round].append(self.main_deck_list[deck_i, pack_i])
                deck_i += pack_i
                pack_i += self.pack_size
        deck_i = 0
        num_e_packs = len(self.extra_deck_list) / (self.pack_size * self.max_players)
        for round in range(0, num_e_packs):
            self.player_e_packs[round] = {round: []}
            for i in range(0, self.max_players):
                self.player_e_packs[round].append(self.extra_deck_list[deck_i, pack_i])
                deck_i += pack_i
                pack_i += self.pack_size

    def get_pack(self, player_id, round):
        return self.player_m_packs.get(round)[player_id]

    def pick_card(self, player_id, card_id):
        player_pack = self.player_m_packs.get(round)[player_id]
        player_pack.remove(card_id)
        self.player_decks[player_id].append(card_id)
        
    
