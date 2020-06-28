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
    draftParams.setMainList(main_list)
    draftParams.setExtraList(main_list)
    draftParams.setPlayerLength(3)
    draftParams.setPackSize(1)
    draftParams.setTimeLimit(3)


class TestDraftService(unittest.TestCase):
    def setUp(self):
        self.main_list = ["1", "2", "3", "4", "5", "6"]
        self.extra_list = ["11", "12", "13", "14", "15", "16"]
        draftParams.setMainList(self.main_list)
        draftParams.setExtraList(self.extra_list)
        draftParams.setPlayerLength(3)
        draftParams.setPackSize(1)
        draftParams.setRoundTime(3)
        self.draftService = DraftService(draftParams)

    def test_init_draft(self):
        assert self.draftService.max_players == 3
        assert self.draftService.main_deck_list == self.main_list
        assert self.draftService.extra_deck_list == self.extra_list
        assert self.draftService.pack_size == 1
        assert self.draftService.time_limit == 3
        assert self.draftService.player_decks == {}
        assert self.draftService.player_e_decks == {}
        assert self.draftService.player_m_packs == {}
        assert self.draftService.player_e_packs == {}

    def test_create_draft(self):
        main_list = list.copy(self.main_list)
        self.draftService.createDraft()
        print(self.main_list)
        print(self.draftService.main_deck_list)
        assert len(self.draftService.player_m_packs) == 2
        assert len(self.draftService.player_e_packs) == 2
        assert self.draftService.main_deck_list != main_list
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.player_m_packs[round][player][0] == self.main_list[round * self.draftService.max_players + player]
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.player_e_packs[round][player][0] == self.extra_list[round * self.draftService.max_players + player]

    def test_get_m_pack(self):
        self.draftService.createDraft()
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.get_m_pack(player, round)[0] == self.main_list[round * self.draftService.max_players + player]

    def test_get_e_pack(self):
        self.draftService.createDraft()
        for round in range(0, 2):
            for player in range(0, self.draftService.max_players):
                assert self.draftService.get_e_pack(player, round)[0] == self.extra_list[round * self.draftService.max_players + player]

    def test_pick_m_card(self):
        self.draftService.createDraft()
        player = 1
        round = 0
        pack = self.draftService.get_m_pack(player, round)
        card_id = pack[0]
        assert len(self.draftService.player_decks) == 0
        self.draftService.pick_m_card(player, round, card_id)
        assert self.draftService.player_decks[player] == [card_id]
        assert len(pack) == 0

    def test_has_all_player_picked(self):
        self.draftService.createDraft()
        round = 0
        for player in range(self.draftService.max_players):
            pack = self.draftService.get_m_pack(player, round)
            self.draftService.pick_m_card(player, round, pack[0])
            assert self.draftService.has_all_players_picked() == (player == self.draftService.max_players - 1)

    def test_rotate_pack(self):
        self.draftService.createDraft()
        packs = list.copy(self.draftService.player_m_packs[0])
        assert self.draftService.player_m_packs[0] == packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_m_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_m_packs[0] == packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_m_packs[0] != packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_m_packs[0] != packs
        self.draftService.rotate_pack(0, "right")
        assert self.draftService.player_m_packs[0] == packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_m_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_m_packs[0] != packs
        self.draftService.rotate_pack(0, "left")
        assert self.draftService.player_m_packs[0] == packs
