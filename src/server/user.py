import hashlib


class User:
    def __init__(self, username, password, salt):
        self._username = username
        self._password = password  # TODO: Remove this when testing is complete with encrypted password
        self._salt = salt
        self._key = self.encrypt_password(password)

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @property
    def salt(self) -> str:
        return self._salt

    @salt.setter
    def salt(self, value: str) -> str:
        self._salt = value

    def __str__(self):
        return f'Username: {self._username} Password: {self._password} Salt: {self._salt} Key: {self._key}'

    def encrypt_password(self, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self._salt, 100000)

    def to_json(self):
        json = {
            "username": self._username,
            "password": self._key,
        }
        return json
