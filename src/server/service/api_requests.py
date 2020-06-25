import requests
import logging
from server.service.ygo_card_db_service import YGOCardDBService

logger = logging.getLogger()
API_URL = "https://db.ygoprodeck.com/api/v6/cardinfo.php"


class APIRequest:
    def populate_card_info_db(db_obj: YGOCardDBService):
        logger.debug(f"Populating Card Info Collection from {API_URL}")
        resp = requests.get(API_URL)
        card_list = resp.json()
        db_obj.insert_cards(card_list)
