
"""
    user_account_db_service.py: This class communicates with MongoDB to operate on the USERS database
    Usage:
        This class holds the basic information to access the USERS database.
        Each user is represented by the User class which this class manages.
"""
import os
import logging
import strings
from mongodb_service import MongoDBService
from user import User

logger = logging.getLogger()


class UserAccountDBService(MongoDBService):
    def __init__(self, database_name: str, collection: str, db_url: str):
        super(UserAccountDBService, self).__init__(database_name, db_url)
        self._cursor = self._database[collection]
        self._collection = collection
        self._salt = os.urandom(32)
        self._key = None

    def __str__(self):
        return f"Client: {self._client} Database: {self._database} Collection: {self._collection} Cursor: {self._cursor}"

    def get_collection(self) -> list:
        resp_list = []
        for document in self._cursor.find():
            resp_list.append(document)
        return resp_list

    def get_user(self, username):
        user = self._cursor.find_one({"username": username})
        return user

    def insert_new_user(self, username, password):
        if self.check_existing_user(username) is True:
            logger.info(f"Username '{username}' was already taken")
            return strings.USERNAME_TAKEN
        user = User(username, password, self._salt)
        self._cursor.insert_one(user.to_json())
        logger.info(f"Created user: '{username}'")
        return strings.SUCCESS

    def check_existing_user(self, username):
        found_existing_user = self._cursor.count_documents({"username": username}, limit=1)
        if found_existing_user == 0:
            return False
        else:
            return True

    def login_user(self, username, password):
        if self.check_existing_user(username) is True:
            user = User(username, password, self._salt)
            given_password = user.encrypt_password(password)
            stored_password = self._cursor.find_one({"username": username})["password"]
            # logger.debug(f"Given password: {given_password}, Stored password: {stored_password}")
            if given_password == stored_password:
                return user
            else:
                return strings.INCORRECT_PASSWORD
        else:
            return strings.USER_NOT_FOUND

    def delete_user(self):
        pass

    def reset_password(self):
        pass

    def verify_user(self):
        pass
