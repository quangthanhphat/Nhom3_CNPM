from infrastructure.models.generated_models import PhotowalkRegistrations
from infrastructure.repositories.photowalk_registration_repository import (
    PhotowalkRegistrationRepository
)
from infrastructure.repositories.photowalk_repository import PhotowalkRepository


class PhotowalkRegistrationService:

    def __init__(self):
        self.repository = PhotowalkRegistrationRepository()
        self.photowalk_repository = PhotowalkRepository()

    def list_for_user(self, user_id, role):
        registrations = self.repository.list_all()

        if role == 'admin':
            return registrations

        if role == 'customer':
            return [
                registration
                for registration in registrations
                if str(registration.user_id) == str(user_id)
            ]

        if role == 'photography_expert':
            result = []

            for registration in registrations:
                photowalk = self.photowalk_repository.get_by_id(
                    registration.photowalk_id
                )

                if (
                    photowalk
                    and str(photowalk.organizer_id) == str(user_id)
                ):
                    result.append(registration)

            return result

        return []

    def get_by_id_for_user(self, registration_id, user_id, role):
        registration = self.repository.get_by_id(
            registration_id
        )

        if not registration:
            return None, 'not_found'

        if role == 'admin':
            return registration, None

        if role == 'customer':
            if str(registration.user_id) != str(user_id):
                return None, 'forbidden'

            return registration, None

        if role == 'photography_expert':
            photowalk = self.photowalk_repository.get_by_id(
                registration.photowalk_id
            )

            if not photowalk:
                return None, 'not_found'

            if str(photowalk.organizer_id) != str(user_id):
                return None, 'forbidden'

            return registration, None

        return None, 'forbidden'

    def create(self, user_id, data):
        photowalk_id = data.get('photowalk_id')

        photowalk = self.photowalk_repository.get_by_id(
            photowalk_id
        )

        if not photowalk:
            return None, 'photowalk_not_found'

        registration = PhotowalkRegistrations(
            photowalk_id=photowalk_id,
            user_id=user_id
        )

        return self.repository.create(registration), None

    def delete(self, registration_id, user_id, role):
        registration, error = self.get_by_id_for_user(
            registration_id=registration_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(registration)

        return True, None