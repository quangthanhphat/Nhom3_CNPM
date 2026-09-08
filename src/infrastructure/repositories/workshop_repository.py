from infrastructure.models.generated_models import Workshops
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class WorkshopRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Workshops).all()

    def get_by_id(self, workshop_id):
        return self.session.query(Workshops).filter(
            Workshops.id == workshop_id
        ).first()

    def create(self, workshop):
        self.session.add(workshop)
        self.session.commit()
        self.session.refresh(workshop)

        return workshop

    def update(self, workshop):
        self.session.commit()
        self.session.refresh(workshop)

        return workshop

    def delete(self, workshop):
        self.session.delete(workshop)
        self.session.commit()