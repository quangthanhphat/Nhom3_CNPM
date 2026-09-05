from infrastructure.models.generated_models import FilmLabs
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class FilmLabRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(FilmLabs).all()

    def get_by_id(self, film_lab_id):
        return self.session.query(FilmLabs).filter(
            FilmLabs.id == film_lab_id
        ).first()

    def create(self, film_lab):
        self.session.add(film_lab)
        self.session.commit()
        self.session.refresh(film_lab)
        return film_lab

    def update(self, film_lab):
        self.session.commit()
        self.session.refresh(film_lab)
        return film_lab

    def delete(self, film_lab):
        self.session.delete(film_lab)
        self.session.commit()