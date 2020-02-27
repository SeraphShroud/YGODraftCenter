class User:
    def __init__(self, username, hashed_password):
        self._username = username
        self._key = hashed_password

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

    def __str__(self):
        return f'Username: {self._username} Key: {self._key}'

    def to_json(self):
        json = {
            "username": self._username,
            "password": self._key,
        }
        return json
