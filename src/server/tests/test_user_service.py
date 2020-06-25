import pytest
import logging
from pymongo import MongoClient
from server.enums.strings import HttpResponse
from server.service.user_account_db_service import UserAccountDBService

TEST_DB_NAME = 'TEST_USERS_DB'
TEST_COLLECTION_NAME = 'TEST_USERS'
TEST_DB_PORT = 27017
TEST_DB_HOST = 'localhost'
TEST_DB_URL = f'mongodb://{TEST_DB_HOST}:{TEST_DB_PORT}'
VALID_USER = 'user1'
VALID_USER_2 = 'hiphophippotomas'
VALID_PASSWORD = 'peopleareangry1'
VALID_PASSWORD_2 = '&4/9Fp`-'
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
        assert resp == HttpResponse.SUCCESS
        actual = cursor.find_one({"username": VALID_USER})
        assert actual["username"] == VALID_USER
        assert actual["password"] != VALID_PASSWORD

    def test_multiple_username_signups(self, cleanup_db):
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == HttpResponse.SUCCESS
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == HttpResponse.USERNAME_TAKEN
        resp = service.insert_new_user(VALID_USER_2, VALID_PASSWORD_2)
        assert resp == HttpResponse.SUCCESS

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
        assert resp == HttpResponse.SUCCESS
        resp = service.login_user(VALID_USER, VALID_PASSWORD)
        actual = cursor.find_one({"username": VALID_USER})
        assert actual["username"] == resp["username"]
        assert actual["password"] == resp["password"]

    def test_valid_username_wrong_pwd(self):
        resp = service.login_user(VALID_USER, WRONG_PASSWORD)
        assert resp == HttpResponse.INCORRECT_PASSWORD

    def test_delete_user(self, cleanup_db):
        resp = service.insert_new_user(VALID_USER, VALID_PASSWORD)
        assert resp == HttpResponse.SUCCESS
        resp = service.delete_user(VALID_USER)
        assert resp == HttpResponse.SUCCESS
        resp = service.delete_user('fakeuser')
        assert resp == HttpResponse.USER_NOT_FOUND

    def test_reset_password(self, cleanup_db):
        resp = service.insert_new_user(VALID_USER, WRONG_PASSWORD)
        assert resp == HttpResponse.SUCCESS

        user_orig = service.get_user(VALID_USER)

        resp = service.reset_password(VALID_USER, VALID_PASSWORD)
        assert resp == HttpResponse.SUCCESS

        user_after = service.get_user(VALID_USER)

        assert user_orig["password"] != user_after["password"]
        assert user_orig["_id"] == user_after["_id"]

    # def test_invalid_username_valid_pwd(self):
    #     pass

    # def test_invalid_username_invalid_pwd(self):
    #     pass

    # def test_signup_weird_chars_username(self):
    #     pass
