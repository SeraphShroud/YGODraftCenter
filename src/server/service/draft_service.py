import random
from models.draft_params import DraftParams


class InvalidMoveError(Exception):
    """Exception Raised when Game move is not Allowed
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DraftService:
    def __init__(self, draft_params: DraftParams, deck_list: list):
        self.max_players = draft_params.get_player_length()
        self.deck_list = deck_list
        self.pack_size = draft_params.get_pack_size()
        self.time_limit = draft_params.get_round_time()
        self.player_decks = {}
        self.player_packs = {}
        self.player_picked = [0 for i in range(self.max_players)]
        self.num_packs = None

    def create_draft(self):
        random.shuffle(self.deck_list)
        num_packs = int(len(self.deck_list) / (self.pack_size * self.max_players))
        self.num_packs = num_packs
        pack_start = 0
        pack_end = self.pack_size
        for round in range(0, num_packs):
            self.player_packs[round] = []
            for player in range(0, self.max_players):
                if pack_end > len(self.deck_list):
                    self.player_packs[round].append(self.deck_list[pack_start:pack_end])
                else:
                    self.player_packs[round].append(self.deck_list[pack_start:pack_end])
                pack_start += self.pack_size
                pack_end += self.pack_size

    def get_pack(self, player_id: int, round: int):
        return self.player_packs[round][player_id]

    def pick_card(self, player_id: int, round: int, card_id: str):
        player_pack = self.player_packs[round][player_id]
        if card_id not in player_pack:
            raise InvalidMoveError("this card is not in your pack")
        player_pack.remove(card_id)
        if player_id in self.player_decks:
            self.player_decks[player_id].append(card_id)
        else:
            self.player_decks[player_id] = [card_id]
        self.player_picked[player_id] = 1

    def has_all_players_picked(self):
        if 0 in self.player_picked:
            return False
        else:
            return True
        
    def rotate_pack(self, round: int, direction: str):
        round_packs = self.player_packs[round]
        if direction == "right":
            # rotate to the right
            self.player_packs[round] = round_packs[-1:] + round_packs[:-1]
        elif direction == "left":
            # rotate to the left
            self.player_packs[round] = round_packs[1:] + round_packs[:1]
        else:
            raise InvalidMoveError("direction was not set correctly")
        # reset the player picked flags for new round
        self.player_picked = [0 for i in range(self.max_players)]

    def get_deck(self, player_id: int):
        return self.player_decks[player_id]

    def has_ended(self, round: int):
        if (self.has_all_players_picked() or self.num_packs == 0) and round == self.num_packs:
            return True
        else:
            return False


        
    
