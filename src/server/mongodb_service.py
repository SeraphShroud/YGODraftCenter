
"""
    mongodb_service.py: A parent class for the Database connection services
    Usage:
        This class holds the basic information to access the yugiohdb database.
        Other subclasses should implement their specific table functions.
"""
from pymongo import MongoClient


"""
SQL Terms/Concepts          MongoDB Terms/Concepts
------------------          ----------------------
database                    database
table                       collection
row                         document or BSON document
column                      field
index                       index
table joins                 $lookup
primary key                 primary key
aggregation (group by)      aggregation pipeline
SELECT INTO NEW_TABLE       $out
MERGE INTO TABLE            $merge
transactions                transactions
"""


class MongoDBService:
    def __init__(self, database_name, db_url):
        self._client = MongoClient(db_url)
        self._database = self._client[database_name]

    def __str__(self):
        return f"Client: {self._client} Database: {self._database}"
