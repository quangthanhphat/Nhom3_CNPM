from infrastructure.models.generated_models import MarketplaceMessages
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class MarketplaceMessageRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(MarketplaceMessages).all()

    def get_by_id(self, message_id):
        return self.session.query(MarketplaceMessages).filter(
            MarketplaceMessages.id == message_id
        ).first()

    def create(self, message):
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    def update(self, message):
        self.session.commit()
        self.session.refresh(message)

        return message

    def delete(self, message):
        self.session.delete(message)
        self.session.commit()