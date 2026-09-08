from infrastructure.models.digital_film_archive_model import DigitalFilmArchiveModel
from infrastructure.repositories.digital_film_archive_repository import (
    DigitalFilmArchiveRepository
)


class DigitalFilmArchiveService:
    def __init__(self):
        self.repository = DigitalFilmArchiveRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        archives = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return archives

        # Customer chỉ xem archive của mình
        if role == 'customer':
            return [
                archive
                for archive in archives
                if str(archive.customer_id) == str(user_id)
            ]

        return []

    def get_by_id(self, archive_id):
        return self.repository.get_by_id(archive_id)

    def get_by_id_for_user(self, archive_id, user_id, role):
        archive = self.repository.get_by_id(archive_id)

        if not archive:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return archive, None

        # Customer chỉ xem archive của mình
        if role == 'customer':
            if str(archive.customer_id) != str(user_id):
                return None, 'forbidden'

            return archive, None

        return None, 'forbidden'

    def create(self, customer_id, data):
        archive = DigitalFilmArchiveModel(
            customer_id=customer_id,
            name=data.get('name'),
            description=data.get('description')
        )

        return self.repository.create(archive)

    def update(
        self,
        archive_id,
        data,
        user_id,
        role
    ):
        archive, error = self.get_by_id_for_user(
            archive_id=archive_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        if 'name' in data:
            archive.name = data.get('name')

        if 'description' in data:
            archive.description = data.get('description')

        return self.repository.update(archive), None

    def delete(
        self,
        archive_id,
        user_id,
        role
    ):
        archive, error = self.get_by_id_for_user(
            archive_id=archive_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(archive)

        return True, None