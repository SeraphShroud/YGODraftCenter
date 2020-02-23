import requests
from mongo_database import MongoDBEngine as db

API_URL = "https://db.ygoprodeck.com/api/v6/cardinfo.php"


def populate_db():
    resp = requests.get(API_URL)
    print(resp)
    card_list = resp.json()
    db.insert_cards(card_list)
