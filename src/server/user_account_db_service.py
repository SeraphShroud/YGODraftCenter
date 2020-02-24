from pymongo import MongoClient
from mongodb_service import MongoDBService


class UserAccountDBService(MongoDBService):
    def __init__(self, database_name, collection, db_url):
        super(UserAccountDBService, self).__init__(database_name, db_url)
        self._cursor = self._database[collection]
        self._collection = collection

    def __str__(self):
        return f"Client: {self._client}\nDatabase: {self._database}\nCollection: {self._collection}\nCursor: {self._cursor}"

    def insert_new_user(self):
        pass

    def delete_user(self):
        pass

    def reset_password(self):
        pass

    def verify_user(self):
        pass
