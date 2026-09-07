from infrastructure.models.generated_models import FilmLabs
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class FilmLabService:
    def __init__(self):
        self.repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, film_lab_id):
        return self.repository.get_by_id(film_lab_id)

    def create(self, owner_id, data):
        film_lab = FilmLabs(
            owner_id=owner_id,
            name=data.get('name'),
            description=data.get('description'),
            city=data.get('city'),
            district=data.get('district'),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get('email')
        )

        return self.repository.create(film_lab)

    def update(self, film_lab_id, data):
        film_lab = self.repository.get_by_id(film_lab_id)

        if not film_lab:
            return None

        film_lab.name = data.get('name', film_lab.name)
        film_lab.description = data.get('description', film_lab.description)
        film_lab.city = data.get('city', film_lab.city)
        film_lab.district = data.get('district', film_lab.district)
        film_lab.address = data.get('address', film_lab.address)
        film_lab.phone = data.get('phone', film_lab.phone)
        film_lab.email = data.get('email', film_lab.email)

        return self.repository.update(film_lab)

    def delete(self, film_lab_id):
        film_lab = self.repository.get_by_id(film_lab_id)

        if not film_lab:
            return False

        self.repository.delete(film_lab)

        return True