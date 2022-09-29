from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO
import hashlib
import base64
import hmac


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, username):
        return self.dao.get_one(username)

    def update(self, up_user, user_name):
        if "password" in up_user:
            up_user["password"] = self.get_hash(up_user["password"])
        return self.dao.update(up_user, user_name)

    def get_hash(self, password):
        d = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(d)

    def compare_passwords(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        )

    def create(self, new_user):
        password = self.get_hash(new_user["password"])
        new_user["password"] = password
        return self.dao.create(new_user)
