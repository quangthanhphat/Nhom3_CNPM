from infrastructure.models.generated_models import MarketplaceListings
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class MarketplaceListingRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(MarketplaceListings).all()

    def get_by_id(self, listing_id):
        return self.session.query(MarketplaceListings).filter(
            MarketplaceListings.id == listing_id
        ).first()

    def create(self, listing):
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(listing)

        return listing

    def update(self, listing):
        self.session.commit()
        self.session.refresh(listing)

        return listing

    def delete(self, listing):
        self.session.delete(listing)
        self.session.commit()