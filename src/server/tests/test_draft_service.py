import pytest
import logging
import os 
# get current directory 
path = os.path.dirname(os.path.abspath(__file__))
# parent directory 
parent = os.path.dirname(path) 
import sys
sys.path.append(parent)
from service.draft_service import DraftService
from models.draft_params import DraftParams
import unittest

draftParams = DraftParams()
logger = logging.getLogger()
draftService = None
main_list = None


@pytest.fixture()
def set_up_draft():
    main_list = ["1", "2", "3", "4", "5", "6"]
    draftParams.set_main_list(main_list)
    draftParams.set_extra_list(main_list)
    draftParams.set_player_length(3)
    draftParams.set_pack_size(1)
    draftParams.setTimeLimit(3)


class TestDraftService(unittest.TestCase):
    def setUp(self):
        self.main_list = ["1", "2", "3", "4", "5", "6"]
        self.extra_list = ["11", "12", "13", "14", "15", "16"]
        draftParams.set_main_list(self.main_list)
        draftParams.set_extra_list(self.extra_list)
        draftParams.set_player_length(3)
        draftParams.set_pack_size(1)
        draftParams.set_round_time(3)
        self.draftService = DraftService(draftParams, draftParams.get_main_list())

    def test_init_draft(self):
        assert self.draftService.max_players == 3
        assert self.draftService.deck_list == self.main_list
        assert self.draftService.pack_size == 1
        assert self.draftService.time_limit == 3
        assert self.draftService.player_decks == {}
        assert self.draftService.player_packs == {}

    def test_create_draft(self):
        main_list = list.copy(self.main_list)
        self.draftService.create_draft()
        print(self.main_list)
        print(self.draftService.deck_list)
        assert len(self.draftService.player_packs) == 2
        assert self.draftService.deck_list != main_list
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.player_packs[round][player][0] == self.main_list[round * self.draftService.max_players + player]

    def test_get_pack(self):
        self.draftService.create_draft()
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.get_pack(player, round)[0] == self.main_list[round * self.draftService.max_players + player]

    def test_pick_card(self):
        self.draftService.create_draft()
        player = 1
        round = 0
        pack = self.draftService.get_pack(player, round)
        card_id = pack[0]
        assert len(self.draftService.player_decks) == 0
        self.draftService.pick_card(player, round, card_id)
        assert self.draftService.player_decks[player] == [card_id]
        assert len(pack) == 0

    def test_has_all_player_picked(self):
        self.draftService.create_draft()
        round = 0
        for player in range(self.draftService.max_players):
            pack = self.draftService.get_pack(player, round)
            self.draftService.pick_card(player, round, pack[0])
            assert self.draftService.has_all_players_picked() == (player == self.draftService.max_players - 1)

    def test_rotate_pack(self):
        self.draftService.create_draft()
        packs = list.copy(self.draftService.player_packs[0])
        assert self.draftService.player_packs[0] == packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_packs[0] == packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_packs[0] != packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_packs[0] != packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_packs[0] == packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_packs[0] == packs
