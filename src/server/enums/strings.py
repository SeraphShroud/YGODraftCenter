class HttpStatus:
    # HTTP Status Codes
    OK_STATUS_CODE = 200
    CREATED_STATUS_CODE = 201
    MOVED_PERMANENTLY_STATUS_CODE = 301
    AUTHORIZATION_ERROR_CODE = 403
    NOT_FOUND_STATUS_CODE = 404
    BAD_REQUEST_STATUS_CODE = 400
    VALIDATION_ERROR_STATUS_CODE = 422
    TOO_MANY_REQUESTS_STATUS_CODE = 429
    INTERNAL_ERROR_STATUS_CODE = 500


class HttpResponse:
    # HTTP Return Strings
    SUCCESS = "Success."
    USERNAME_TAKEN = "Username already exists."
    USER_NOT_FOUND = "Username does not exist."
    INCORRECT_PASSWORD = "Password is incorrect."


class MongoDB:
    DB_HOST = "localhost"
    DB_PORT = 27017
    DB_URL = f"mongodb://{DB_HOST}:{DB_PORT}"
    DB_NAME = "yugioh_db"
    CARD_COLLECTION_NAME = "card_info"


class Draft:
    KEY = "draft"
    DECK = "deck"
    PACK = "pack"
    EXTRA = "#extra"


class YGODraft:
    ROUND = "draft_round"
    GAME = "ygo_draft"
    PARAM = "draft_param"
    MAIN = "main_draft"
    EXTRA = "extra_draft"
    NAME= "draft_name"

