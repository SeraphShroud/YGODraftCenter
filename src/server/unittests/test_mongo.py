import pytest
from pymongo import MongoClient
from server.mongo_database import MongoDBEngine as db

TEST_DB_PORT = 25555

card_1 = {
    "id": 6983839,
    "name": "Tornado Dragon",
    "type": "XYZ Monster",
    "desc": "2 Level 4 monsters Once per turn, during either player's turn: You can detach 1 Xyz Material from this card, then target 1 Spell/Trap Card on the field; destroy it."
}
card_2 = {
    "id": 34541863,
    "name": "\"A\" Cell Breeding Device",
    "type": "Spell Card",
    "desc": "During each of your Standby Phases, put 1 A-Counter on 1 face-up monster your opponent controls."
}
id_list = [
    77235086,
    25857246
]

card_list = [card_1, card_2]
pytest.db = None


@pytest.fixture(scope="session")
def setup_db():
    client = MongoClient('localhost', TEST_DB_PORT)
    pytest.db = client["yugiohdb"]


@pytest.fixture(scope="session", autouse=True)
def insert_basic_data(setup_db):
    collection = pytest.db["card_info"]
    for card in card_list:
        collection.insert(card)


class TestMongoDB:
    def test_get_collection(setup_db):
        pass

    def test_insert_card_info(self):
        db.insert_card_info(card_1)
        pass

    def test_insert_cards(self):
        pass

    def test_delete_card_info(self):
        pass

    def test_get_card_list(self):
        pass
