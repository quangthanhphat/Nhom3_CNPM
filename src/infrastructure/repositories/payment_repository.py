from infrastructure.models.generated_models import Payments
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class PaymentRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Payments).all()

    def get_by_id(self, payment_id):
        return self.session.query(Payments).filter(
            Payments.id == payment_id
        ).first()

    def create(self, payment):
        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)
        return payment

    def update(self, payment):
        self.session.commit()
        self.session.refresh(payment)
        return payment

    def delete(self, payment):
        self.session.delete(payment)
        self.session.commit()