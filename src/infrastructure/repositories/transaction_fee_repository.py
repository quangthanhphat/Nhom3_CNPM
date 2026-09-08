from infrastructure.models.generated_models import TransactionFees
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class TransactionFeeRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(TransactionFees).all()

    def get_by_id(self, fee_id):
        return self.session.query(TransactionFees).filter(
            TransactionFees.id == fee_id
        ).first()

    def create(self, fee):
        self.session.add(fee)
        self.session.commit()
        self.session.refresh(fee)

        return fee

    def update(self, fee):
        self.session.commit()
        self.session.refresh(fee)

        return fee

    def delete(self, fee):
        self.session.delete(fee)
        self.session.commit()