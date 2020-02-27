import requests
from ygo_card_db_service import YGOCardDBService

API_URL = "https://db.ygoprodeck.com/api/v6/cardinfo.php"


def populate_card_info_db(db_obj: YGOCardDBService):
    resp = requests.get(API_URL)
    card_list = resp.json()
    db_obj.insert_cards(card_list)
