from infrastructure.models.support_model import SupportModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class SupportRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return (
            self.session.query(SupportModel)
            .order_by(SupportModel.created_at.desc())
            .all()
        )

    def list_by_user(self, user_id):
        return (
            self.session.query(SupportModel)
            .filter(SupportModel.user_id == user_id)
            .order_by(SupportModel.created_at.desc())
            .all()
        )

    def find_by_id(self, support_id):
        return (
            self.session.query(SupportModel)
            .filter(SupportModel.id == support_id)
            .first()
        )

    def create(self, support):
        self.session.add(support)
        self.session.commit()
        self.session.refresh(support)
        return support

    def update(self, support):
        self.session.commit()
        self.session.refresh(support)
        return support

    def delete(self, support):
        self.session.delete(support)
        self.session.commit()