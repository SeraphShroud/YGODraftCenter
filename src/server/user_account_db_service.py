
"""
    user_account_db_service.py: This class communicates with MongoDB to operate on the USERS database
    Usage:
        This class holds the basic information to access the USERS database.
        Each user is represented by the User class which this class manages.
"""
import os
import logging
import strings
import hashlib
from mongodb_service import MongoDBService
from user import User

logger = logging.getLogger()


class UserAccountDBService(MongoDBService):
    def __init__(self, database_name: str, collection: str, db_url: str):
        super(UserAccountDBService, self).__init__(database_name, db_url)
        self._cursor = self._database[collection]
        self._collection = collection
        self._salt = b'\xae\xf6\x93\xb3\x1b\x8a;o\x02\x8dC\xffN\xa4\xacJ4\xfb\xb2e!w\x0f\x1b\x15\xfb&\xc8C(\xa80'

    def __str__(self):
        return f"Client: {self._client} Database: {self._database} Collection: {self._collection} Cursor: {self._cursor}"

    def encrypt_password(self, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self._salt, 100000)

    def get_collection(self) -> list:
        resp_list = []
        for document in self._cursor.find():
            resp_list.append(document)
        return resp_list

    def get_user(self, username):
        user = self._cursor.find_one({"username": username})
        return user

    def insert_new_user(self, username, password) :
        if self.check_existing_user(username) is True:
            logger.info(f"Username '{username}' was already taken")
            return strings.USERNAME_TAKEN
        hashed_password = self.encrypt_password(password)
        user = User(username, hashed_password)
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
            hashed_password = self.encrypt_password(password)
            user_json = self._cursor.find_one({"username": username})
            # logger.debug(f"Given password: {given_password}, Stored password: {stored_password}")
            if hashed_password == user_json["password"]:
                return user_json
            else:
                return strings.INCORRECT_PASSWORD
        else:
            return strings.USER_NOT_FOUND

    def delete_user(self, username):
        if self.check_existing_user(username) is True:
            self._cursor.delete_one({"username": username})
            return strings.SUCCESS
        else:
            return strings.USER_NOT_FOUND

    def reset_password(self, username, new_password):
        if self.check_existing_user(username) is True:
            hashed_password = self.encrypt_password(new_password)
            primary_key = {"username": username}
            new_values = {"$set": {"password": hashed_password}}
            upsert = True

            self._cursor.update_one(primary_key, new_values, upsert)
            return strings.SUCCESS
        else:
            return strings.USER_NOT_FOUND
