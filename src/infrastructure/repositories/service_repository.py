from infrastructure.models.generated_models import Services
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class ServiceRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Services).all()

    def get_by_id(self, service_id):
        return self.session.query(Services).filter(
            Services.id == service_id
        ).first()

    def create(self, service):
        self.session.add(service)
        self.session.commit()
        self.session.refresh(service)
        return service

    def update(self, service):
        self.session.commit()
        self.session.refresh(service)
        return service

    def delete(self, service):
        self.session.delete(service)
        self.session.commit()