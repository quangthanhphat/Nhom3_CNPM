from infrastructure.models.generated_models import Complaints
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class ComplaintRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Complaints).all()

    def get_by_id(self, complaint_id):
        return self.session.query(Complaints).filter(
            Complaints.id == complaint_id
        ).first()

    def get_by_user_id(self, user_id):
        return self.session.query(Complaints).filter(
            Complaints.user_id == user_id
        ).all()

    def create(self, complaint):
        self.session.add(complaint)
        self.session.commit()
        self.session.refresh(complaint)

        return complaint

    def update(self, complaint):
        self.session.commit()
        self.session.refresh(complaint)

        return complaint

    def delete(self, complaint):
        self.session.delete(complaint)
        self.session.commit()