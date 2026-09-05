from infrastructure.models.generated_models import Orders
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class OrderRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Orders).all()

    def get_by_id(self, order_id):
        return self.session.query(Orders).filter(
            Orders.id == order_id
        ).first()

    def create(self, order):
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def update(self, order):
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order):
        self.session.delete(order)
        self.session.commit()