from infrastructure.models.generated_models import Ratings
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class RatingRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Ratings).all()

    def get_by_id(self, rating_id):
        return self.session.query(Ratings).filter(
            Ratings.id == rating_id
        ).first()

    def create(self, rating):
        self.session.add(rating)
        self.session.commit()
        self.session.refresh(rating)

        return rating

    def update(self, rating):
        self.session.commit()
        self.session.refresh(rating)

        return rating

    def delete(self, rating):
        self.session.delete(rating)
        self.session.commit()