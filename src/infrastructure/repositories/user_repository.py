from infrastructure.models.user_model import UserModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class UserRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def create(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_username(self, username):
        return (
            self.session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )

    def find_by_email(self, email):
        return (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    def find_by_id(self, user_id):
        return (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )