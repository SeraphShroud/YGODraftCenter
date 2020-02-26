import pytest
import logging
import sys
import os
sys.path.append("..")
from user import User

TEST_USERNAME = 'test123'
TEST_PASSWORD = 'passw0rd5'
SALT = os.urandom(32)
user = None

logger = logging.getLogger()


@pytest.fixture(scope="session", autouse=True)
def create_user():
    global user
    user = User(TEST_USERNAME, TEST_PASSWORD, SALT)


class TestUser:
    def test_encrypt_password(self):
        logger.info(user)
        assert TEST_PASSWORD != user.key
        assert user.encrypt_password(TEST_PASSWORD) == user.key
