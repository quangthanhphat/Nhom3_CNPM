from infrastructure.models.generated_models import Favorites
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class FavoriteRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Favorites).all()

    def get_by_id(self, favorite_id):
        return self.session.query(Favorites).filter(
            Favorites.id == favorite_id
        ).first()

    def create(self, favorite):
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)

        return favorite

    def delete(self, favorite):
        self.session.delete(favorite)
        self.session.commit()

        return True