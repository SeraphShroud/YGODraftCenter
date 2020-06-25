import pytest
import logging
from server.service.draft_service import DraftService
from server.models.draft_params import DraftParams
import unittest

draftParams = DraftParams()
logger = logging.getLogger()
draftService = None
main_list = None


@pytest.fixture()
def set_up_draft():
    main_list = [1, 2, 3, 4, 5, 6]
    draftParams.setMainList(main_list)
    draftParams.setExtraList(main_list)
    draftParams.setPlayerLength(3)
    draftParams.setPackSize(1)
    draftParams.setTimeLimit(3)


class TestDraftService(unittest.TestCase):
    def setUp(self):
        self.main_list = [1, 2, 3, 4, 5, 6]
        draftParams.setMainList(self.main_list)
        draftParams.setExtraList(self.main_list)
        draftParams.setPlayerLength(3)
        draftParams.setPackSize(1)
        draftParams.setRoundTime(3)

    def test_init_draft(self):
        draftService = DraftService(draftParams)
        assert draftService.max_players == 3
        assert draftService.main_deck_list == self.main_list
        assert draftService.extra_deck_list == self.main_list
        assert draftService.pack_size == 1
        assert draftService.time_limit == 3
        assert draftService.player_decks == {}
        assert draftService.player_e_decks == {}
        assert draftService.player_m_packs == {}
        assert draftService.player_e_packs == {}
