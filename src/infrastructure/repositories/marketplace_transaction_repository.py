from infrastructure.models.generated_models import MarketplaceTransactions
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class MarketplaceTransactionRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(MarketplaceTransactions).all()

    def get_by_id(self, transaction_id):
        return self.session.query(
            MarketplaceTransactions
        ).filter(
            MarketplaceTransactions.id == transaction_id
        ).first()

    def create(self, transaction):
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)

        return transaction

    def update(self, transaction):
        self.session.commit()
        self.session.refresh(transaction)

        return transaction

    def delete(self, transaction):
        self.session.delete(transaction)
        self.session.commit()