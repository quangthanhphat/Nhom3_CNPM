from infrastructure.models.generated_models import Photowalks
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class PhotowalkRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Photowalks).all()

    def get_by_id(self, photowalk_id):
        return self.session.query(Photowalks).filter(
            Photowalks.id == photowalk_id
        ).first()

    def create(self, photowalk):
        self.session.add(photowalk)
        self.session.commit()
        self.session.refresh(photowalk)

        return photowalk

    def update(self, photowalk):
        self.session.commit()
        self.session.refresh(photowalk)

        return photowalk

    def delete(self, photowalk):
        self.session.delete(photowalk)
        self.session.commit()