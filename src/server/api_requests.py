import requests

API_URL = "https://db.ygoprodeck.com/api/v6/cardinfo.php"


def populate_card_info_db(db_obj):
    resp = requests.get(API_URL)
    print(resp)
    card_list = resp.json()
    db_obj.insert_cards(card_list)
