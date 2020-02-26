import pytest
import json
import logging
import sys
from pymongo import MongoClient
import api_requests
sys.path.append("..")
from server.ygo_card_db_service import YGOCardDBService

logger = logging.getLogger()

TEST_DB_NAME = 'TEST_YUGIOH_DB'
TEST_COLLECTION_NAME = 'TEST_CARD_INFO'
TEST_DB_PORT = 27017
TEST_DB_HOST = 'localhost'
TEST_DB_URL = f'mongodb://{TEST_DB_HOST}:{TEST_DB_PORT}'
client = None
db = None
cursor = None
ygodb = None
two_card_list = []
single_card = {}
four_card_list = []
malformed_card = {}


@pytest.fixture()
def cleanup_db():
    client.drop_database(TEST_DB_NAME)


@pytest.fixture(scope="session", autouse=True)
def create_control_files():
    global two_card_list, single_card, four_card_list, malformed_card
    with open('card_jsons/2_cards_spell_trap.json', 'r') as f:
        result = json.load(f)
    two_card_list = [result]
    with open('card_jsons/1_card_link.json', 'r') as f:
        single_card = json.load(f)
    with open('card_jsons/4_cards_correct.json', 'r') as f:
        result = json.load(f)
    four_card_list = [result]
    with open('card_jsons/1_card_no_id.json', 'r') as f:
        malformed_card = json.load(f)


@pytest.fixture(scope="session", autouse=True)
def cleanup_and_setup_db():
    global client, db, cursor, ygodb
    client = MongoClient(TEST_DB_URL)
    client.drop_database(TEST_DB_NAME)
    db = client[TEST_DB_NAME]
    cursor = db[TEST_COLLECTION_NAME]
    ygodb = YGOCardDBService(TEST_DB_NAME, TEST_COLLECTION_NAME, TEST_DB_URL)


@pytest.fixture()
def insert_basic_data():
    with open('card_jsons/4_cards_correct.json', 'r') as f:
        card_json = json.load(f)
        # logger.debug(card_json)
    cursor.insert_many(card_json)


class TestYGOCardDBService:
    def test_get_collection_empty(self, cleanup_db):
        control_list = []
        actual = ygodb.get_collection()
        assert actual == control_list

    def test_get_collection(self, insert_basic_data):
        control_list = []
        for document in cursor.find():
            control_list.append(document)
        actual = ygodb.get_collection()
        assert actual == control_list

    def test_get_card_list(self):
        test_id_list = [1861629, 85852291]
        control_list = []
        result = cursor.find({"id": {"$in": test_id_list}})
        for card in result:
            control_list.append(card)
        actual = ygodb.get_card_list(test_id_list)
        assert actual == control_list

    def test_get_card_list_bad_list(self):
        bad_id_list = [186, "dga1"]
        control_list = []
        result = cursor.find({"id": {"$in": bad_id_list}})
        for card in result:
            control_list.append(card)
        actual = ygodb.get_card_list(bad_id_list)
        assert actual == control_list

    def test_get_card_list_empty_list(self):
        empty_id_list = []
        control_list = []
        result = cursor.find({"id": {"$in": empty_id_list}})
        for card in result:
            control_list.append(card)
        actual = ygodb.get_card_list(empty_id_list)
        assert actual == control_list

    def test_insert_card_info(self, cleanup_db):
        ygodb.insert_card_info(single_card)
        actual = cursor.find_one(single_card)
        assert actual["id"] == 1861629
        assert actual["name"] == "Decode Talker"

    def test_populate_database(self, cleanup_db):
        api_requests.populate_card_info_db(ygodb)
        actual_card_count = cursor.estimated_document_count()
        assert actual_card_count > 10495

    # def test_insert_cards(self):
    #     pprint(two_card_list)
    #     ygodb.insert_cards(two_card_list)
    #     actual = cursor.find(two_card_list)
    #     pprint(actual)
    #     assert actual == two_card_list

    # def test_insert_card_info(self, cleanup_db):
    #     pass

    # def test_insert_cards(self):
    #     pass

    # def test_delete_card_info(self):
    #     pass
