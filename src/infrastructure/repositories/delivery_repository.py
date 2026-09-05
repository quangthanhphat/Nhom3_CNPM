from infrastructure.models.generated_models import Deliveries
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class DeliveryRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Deliveries).all()

    def get_by_id(self, delivery_id):
        return self.session.query(Deliveries).filter(
            Deliveries.id == delivery_id
        ).first()

    def create(self, delivery):
        self.session.add(delivery)
        self.session.commit()
        self.session.refresh(delivery)
        return delivery

    def update(self, delivery):
        self.session.commit()
        self.session.refresh(delivery)
        return delivery

    def delete(self, delivery):
        self.session.delete(delivery)
        self.session.commit()