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
