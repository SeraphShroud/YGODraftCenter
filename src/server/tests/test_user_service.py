import pytest
import logging
import sys
from pymongo import MongoClient
sys.path.append("..")
import strings
from server.user_account_db_service import UserAccountDBService

TEST_DB_NAME = 'TEST_USERS_DB'
TEST_COLLECTION_NAME = 'TEST_USERS'
TEST_DB_PORT = 27017
TEST_DB_HOST = 'localhost'
TEST_DB_URL = f'mongodb://{TEST_DB_HOST}:{TEST_DB_PORT}'
VALID_USER = 'user1'
VALID_PASSWORD = 'peopleareangry1'
WRONG_PASSWORD = '0921'
client = None
db = None
cursor = None
service = None

logger = logging.getLogger()


@pytest.fixture()
def cleanup_db():
    client.drop_database(TEST_DB_NAME)


@pytest.fixture(scope="session", autouse=True)
def cleanup_and_setup_db():
    global client, db, cursor, service
    client = MongoClient(TEST_DB_URL)
    client.drop_database(TEST_DB_NAME)
    db = client[TEST_DB_NAME]
    cursor = db[TEST_COLLECTION_NAME]
    service = UserAccountDBService(TEST_DB_NAME, TEST_COLLECTION_NAME, TEST_DB_URL)


class TestUserAccountService:
    def test_valid_username_pwd(self):
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == strings.SUCCESS
        actual = cursor.find_one({"username": VALID_USER})
        assert actual["username"] == VALID_USER
        assert actual["password"] != VALID_PASSWORD

    def test_multiple_username_signups(self, cleanup_db):
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == strings.SUCCESS
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == strings.USERNAME_TAKEN
        resp = service.insert_new_user('user2', 'simplepw')
        assert resp == strings.SUCCESS

    def test_get_collection(self):
        control_list = []
        for document in cursor.find():
            control_list.append(document)
        actual = service.get_collection()
        assert actual == control_list

    def test_get_single_user(self):
        control = cursor.find_one({"username": VALID_USER})
        assert control == service.get_user(VALID_USER)

    def test_successful_login(self, cleanup_db):
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == strings.SUCCESS
        resp = service.login_user(VALID_USER, VALID_PASSWORD)
        actual = cursor.find_one({"username": VALID_USER})
        assert actual['username'] == resp.username
        assert actual['password'] == resp.key

    def test_valid_username_wrong_pwd(self):
        resp = service.login_user(VALID_USER, WRONG_PASSWORD)
        assert resp == strings.INCORRECT_PASSWORD

    def test_invalid_username_valid_pwd(self):
        pass

    def test_invalid_username_invalid_pwd(self):
        pass

    def test_signup_weird_chars_username(self):
        pass
