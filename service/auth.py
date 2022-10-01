import calendar
import datetime
from config import Config
import jwt
from flask import abort, request
from conteiner import UserService

c = Config()
SECRET_HERE = c.SECRET_HERE
ALGORITHM = c.ALGORITHM


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_one(username)

        if user is None:
            raise abort(401)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }
        mins30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(mins30.timetuple())
        access_token = jwt.encode(data, SECRET_HERE, algorithm=ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET_HERE, algorithm=ALGORITHM)

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return tokens

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=SECRET_HERE, allgorithms=ALGORITHM)
        username = data.get("username")

        return self.generate_token(username, None, is_refresh=True)


    def auth_required(self, func):
        def wrapper(*args, **kwargs):
            if "Authorization" not in request.headers:
                abort(401)

            data = request.headers["Authorization"]
            token = data.split('Bearer ')[-1]
            try:
                d = jwt.decode(token, c.SECRET_HERE, algorithms=[ALGORITHM])
                role = d.get("role")
                if role != "admin":
                    abort(403)
            except Exception as e:
                print(e)
                abort(401)


            return func(*args, **kwargs)
        return wrapper