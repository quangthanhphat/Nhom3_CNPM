from infrastructure.models.generated_models import WorkshopRegistrations
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class WorkshopRegistrationRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(WorkshopRegistrations).all()

    def get_by_id(self, registration_id):
        return self.session.query(WorkshopRegistrations).filter(
            WorkshopRegistrations.id == registration_id
        ).first()

    def create(self, registration):
        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)

        return registration

    def update(self, registration):
        self.session.commit()
        self.session.refresh(registration)

        return registration

    def delete(self, registration):
        self.session.delete(registration)
        self.session.commit()