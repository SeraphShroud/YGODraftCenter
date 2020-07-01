import random
from models.draft_params import DraftParams


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
        self.player_picked = [0 for i in range(self.max_players)]
        self.num_packs = None

    def createDraft(self):
        random.shuffle(self.main_deck_list)
        random.shuffle(self.extra_deck_list)
        num_packs = int(len(self.main_deck_list) / (self.pack_size * self.max_players))
        self.num_packs = num_packs
        pack_start = 0
        pack_end = self.pack_size
        for round in range(0, num_packs):
            start_i = round * self.max_players
            self.player_m_packs[round] = []
            for player in range(0, self.max_players):
                if pack_end > len(self.main_deck_list):
                    self.player_m_packs[round].append(self.main_deck_list[pack_start:pack_end])
                else:
                    self.player_m_packs[round].append(self.main_deck_list[pack_start:pack_end])
                pack_start += self.pack_size
                pack_end += self.pack_size
        num_e_packs = int(len(self.extra_deck_list) / (self.pack_size * self.max_players))
        for round in range(0, num_e_packs):
            start_i = round * self.max_players
            self.player_e_packs[round] = [self.extra_deck_list[i:i + self.pack_size] for i in range(start_i, start_i + self.max_players, self.pack_size)]

    def get_m_pack(self, player_id: int, round: int):
        return self.player_m_packs[round][player_id]

    def get_e_pack(self, player_id: int, round: int):
        return self.player_e_packs[round][player_id]

    def pick_m_card(self, player_id: int, round: int, card_id: str):
        player_pack = self.player_m_packs[round][player_id]
        if card_id not in player_pack:
            raise InvalidMoveError("this card is not in your pack")
        player_pack.remove(card_id)
        if player_id in self.player_decks:
            self.player_decks[player_id].append(card_id)
        else:
            self.player_decks[player_id] = [card_id]
        self.player_picked[player_id] = 1

    def pick_e_card(self, player_id: int, round: int, card_id: str):
        player_pack = self.player_e_packs[round][player_id]
        player_pack.remove(card_id)
        if player_id in self.player_decks:
            self.player_e_decks[player_id].append(card_id)
        else:
            self.player_e_decks[player_id] = [card_id]
        self.player_picked[player_id] = 1

    def has_all_players_picked(self):
        if 0 in self.player_picked:
            return False
        else:
            return True
        
    def rotate_pack(self, round: int, direction: str):
        round_packs = self.player_m_packs[round]
        if direction == "right":
            # rotate to the right
            self.player_m_packs[round] = round_packs[-1:] + round_packs[:-1]
        elif direction == "left":
            # rotate to the left
            self.player_m_packs[round] = round_packs[1:] + round_packs[:1]
        else:
            raise InvalidMoveError("direction was not set correctly")
        # reset the player picked flags for new round
        self.player_picked = [0 for i in range(self.max_players)]

    def get_deck(self, player_id: int):
        return self.player_decks[player_id]

    def has_ended(self, round: int):
        if self.has_all_players_picked() and round == self.num_packs:
            return True
        else:
            return False


        
    
