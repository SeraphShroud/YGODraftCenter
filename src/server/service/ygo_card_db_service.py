from service.mongodb_service import MongoDBService


class YGOCardDBService(MongoDBService):
    def __init__(self, database_name: str, collection: str, db_url: str):
        super(YGOCardDBService, self).__init__(database_name, db_url)
        self._cursor = self._database[collection]
        self._collection = collection

    def __str__(self):
        return f"Client: {self._client} Database: {self._database} Collection: {self._collection} Cursor: {self._cursor}"

    def get_collection(self) -> list:
        return [document for document in self._cursor.find()]

    def get_card_list(self, id_list: list) -> list:
        """
        Summary:
            Retrieves the card information from yugioh card list table.
        Usage:
            Called by the server when a user wants to create a draft.
        Args:
            id_list (list): list representing the IDs of the card needed in the draft.
        Raises:
            MalformedListError TODO: Implement the exception class structure
        Return:
            card_list (list): a list of dictionaries for the card information
        """
        return [card for card in self._cursor.find({"id": {"$in": id_list}})]

    def insert_card_info(self, card: dict):
        """
        Summary:
            Inserts a single card into the card_info table. This will NOT insert
            duplicate cards with the same card ID.
        Usage:
            Called by the server when updating the card_info table with erratas or
            new cards.
        Args:
            card (dict): a single card with the card information from the API.
        Raises:
            MalformedCardError TODO: Implement the exception class structure
        Return:
            None
        """
        primary_key = {"id": card["id"]}
        new_values = {"$set": card}
        upsert = True

        self._cursor.update_many(primary_key, new_values, upsert)

    def insert_cards(self, card_list: list):
        """
        Summary:
            Inserts a list of cards into the card_info table. DO NOT call this
            method if there is a risk of duplicates. Use insert_card_info() instead.
        Usage:
            Called by the server when updating the card_info table for new cards.
        Args:
            card_list (list): a list of dictionaries with card information from the API.
        Raises:
            MalformedListError TODO: Implement the exception class structure
        Return:
            None
        """
        self._cursor.insert_many(card_list)

    def delete_card_info(self, card: dict):
        """
        Summary:
            Deletes all entries of a single card from the card_info table.
        Usage:
            Called by the server when updating the card_info table for new cards.
            This removes all duplicates of a card.
        Args:
            card (dict): a single card with the card information from the API.
        Raises:
            MalformedCardError TODO: Implement the exception class structure
        Return:
            None
        """
        self._cursor.delete_many(card)
