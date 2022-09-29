from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_one(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def update(self, up_user, user_name):
        user = self.get_one(user_name)
        if self.get_one(up_user["username"]) == None:
            if "username" in up_user:
                user.username = up_user["username"]
        if "role" in up_user:
            user.role = up_user["role"]
        if "password" in up_user:
            user.password = up_user["password"]

        self.session.add(user)
        self.session.commit()

    def create(self, new_user):
        with self.session.begin():
            if self.get_one(new_user['username']) == None:
                user = User(**new_user)
                self.session.add(user)
