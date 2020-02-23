from pymongo import MongoClient
from pprint import pprint

DB_URL = "mongodb://localhost:27017"


class MongoDBEngine:

    @staticmethod
    def get_collection(collection: str) -> list:
        client = MongoClient(DB_URL)
        db = client["yugiohdb"]
        cursor = db[collection].find()

        resp_list = []
        for document in cursor:
            resp_list.append(document)
        return resp_list

    @staticmethod
    def insert_card_info(card: dict) -> str:
        client = MongoClient(DB_URL)
        db = client["yugiohdb"]
        collection = db["card_info"]

        primary_key = {"id": card["id"]}
        new_values = {"$set": card}
        upsert = True

        result = collection.update(primary_key, new_values, upsert)
        pprint(result)

    @staticmethod
    def insert_cards(card_list: list):
        client = MongoClient(DB_URL)
        db = client["yugiohdb"]
        collection = db["card_info"]
        for card in card_list:
            primary_key = {"id": card["id"]}
            values = {"$set": card}
            upsert = True

            result = collection.update(primary_key, values, upsert)
            pprint(result)

    @staticmethod
    def delete_card_info(card: dict):
        client = MongoClient(DB_URL)
        db = client["yugiohdb"]
        collection = db["card_info"]
        result = collection.delete_many(card)
        pprint(result)

    @staticmethod
    def get_card_list(id_list: list) -> list:
        client = MongoClient(DB_URL)
        db = client["yugiohdb"]
        collection = db["card_info"]

        card_list = []
        for id in id_list:
            result = collection.find({"id": id})
            for card_info in result:
                card_list.append(card_info)
        print(card_list)
