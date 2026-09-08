from infrastructure.models.generated_models import WorkshopRegistrations
from infrastructure.repositories.workshop_registration_repository import (
    WorkshopRegistrationRepository
)
from infrastructure.repositories.workshop_repository import WorkshopRepository


class WorkshopRegistrationService:

    def __init__(self):
        self.repository = WorkshopRegistrationRepository()
        self.workshop_repository = WorkshopRepository()

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
                workshop = self.workshop_repository.get_by_id(
                    registration.workshop_id
                )

                if (
                    workshop
                    and str(workshop.organizer_id) == str(user_id)
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
            workshop = self.workshop_repository.get_by_id(
                registration.workshop_id
            )

            if not workshop:
                return None, 'not_found'

            if str(workshop.organizer_id) != str(user_id):
                return None, 'forbidden'

            return registration, None

        return None, 'forbidden'

    def create(self, user_id, data):
        workshop_id = data.get('workshop_id')

        workshop = self.workshop_repository.get_by_id(
            workshop_id
        )

        if not workshop:
            return None, 'workshop_not_found'

        registration = WorkshopRegistrations(
            workshop_id=workshop_id,
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
        