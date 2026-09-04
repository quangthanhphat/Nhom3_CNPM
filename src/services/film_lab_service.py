from infrastructure.repositories.film_lab_repository import FilmLabRepository


class FilmLabService:
    def __init__(self):
        self.repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, film_lab_id):
        return self.repository.get_by_id(film_lab_id)