from infrastructure.models.generated_models import Photowalks
from infrastructure.repositories.photowalk_repository import PhotowalkRepository


class PhotowalkService:

    def __init__(self):
        self.repository = PhotowalkRepository()

    def list_for_user(self, user_id, role):
        photowalks = self.repository.list_all()

        if role == 'admin':
            return photowalks

        if role in [
            'customer',
            'film_lab_owner',
            'delivery_partner'
        ]:
            return photowalks

        if role == 'photography_expert':
            return [
                photowalk
                for photowalk in photowalks
                if str(photowalk.organizer_id) == str(user_id)
            ]

        return []

    def get_by_id_for_user(self, photowalk_id, user_id, role):
        photowalk = self.repository.get_by_id(photowalk_id)

        if not photowalk:
            return None, 'not_found'

        if role == 'admin':
            return photowalk, None

        if role in [
            'customer',
            'film_lab_owner',
            'delivery_partner'
        ]:
            return photowalk, None

        if role == 'photography_expert':
            if str(photowalk.organizer_id) != str(user_id):
                return None, 'forbidden'

            return photowalk, None

        return None, 'forbidden'

    def create(self, organizer_id, data):
        photowalk = Photowalks(
            organizer_id=organizer_id,
            title=data.get('title'),
            description=data.get('description'),
            location=data.get('location'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            capacity=data.get('capacity'),
            status=data.get('status', 'open')
        )

        return self.repository.create(photowalk)

    def update(self, photowalk_id, data, user_id, role):
        photowalk, error = self.get_by_id_for_user(
            photowalk_id=photowalk_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        if role != 'admin':
            if str(photowalk.organizer_id) != str(user_id):
                return None, 'forbidden'

        if 'title' in data:
            photowalk.title = data.get('title')

        if 'description' in data:
            photowalk.description = data.get('description')

        if 'location' in data:
            photowalk.location = data.get('location')

        if 'start_time' in data:
            photowalk.start_time = data.get('start_time')

        if 'end_time' in data:
            photowalk.end_time = data.get('end_time')

        if 'capacity' in data:
            photowalk.capacity = data.get('capacity')

        if 'status' in data:
            photowalk.status = data.get('status')

        return self.repository.update(photowalk), None

    def delete(self, photowalk_id, user_id, role):
        photowalk, error = self.get_by_id_for_user(
            photowalk_id=photowalk_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        if role != 'admin':
            if str(photowalk.organizer_id) != str(user_id):
                return False, 'forbidden'

        self.repository.delete(photowalk)

        return True, None