from infrastructure.models.digital_film_archive_model import DigitalFilmArchiveModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class DigitalFilmArchiveRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(DigitalFilmArchiveModel).all()

    def get_by_id(self, archive_id):
        return self.session.query(DigitalFilmArchiveModel).filter(
            DigitalFilmArchiveModel.id == archive_id
        ).first()

    def create(self, archive):
        self.session.add(archive)
        self.session.commit()
        self.session.refresh(archive)
        return archive

    def update(self, archive):
        self.session.commit()
        self.session.refresh(archive)
        return archive

    def delete(self, archive):
        self.session.delete(archive)
        self.session.commit()