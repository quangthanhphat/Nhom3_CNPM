from infrastructure.models.generated_models import Workshops
from infrastructure.repositories.workshop_repository import WorkshopRepository


class WorkshopService:

    def __init__(self):
        self.repository = WorkshopRepository()

    def list_for_user(self, user_id, role):
        workshops = self.repository.list_all()

        # Admin xem tất cả
        if role == 'admin':
            return workshops

        # Customer, Film Lab Owner, Delivery Partner xem tất cả
        if role in [
            'customer',
            'film_lab_owner',
            'delivery_partner'
        ]:
            return workshops

        # Photography Expert chỉ xem workshop của mình
        if role == 'photography_expert':
            return [
                workshop
                for workshop in workshops
                if str(workshop.organizer_id) == str(user_id)
            ]

        return []

    def get_by_id_for_user(self, workshop_id, user_id, role):
        workshop = self.repository.get_by_id(workshop_id)

        if not workshop:
            return None, 'not_found'

        # Admin xem tất cả
        if role == 'admin':
            return workshop, None

        # Các role này được xem tất cả workshop
        if role in [
            'customer',
            'film_lab_owner',
            'delivery_partner'
        ]:
            return workshop, None

        # Photography Expert chỉ xem workshop của mình
        if role == 'photography_expert':
            if str(workshop.organizer_id) != str(user_id):
                return None, 'forbidden'

            return workshop, None

        return None, 'forbidden'

    def create(self, organizer_id, data):
        workshop = Workshops(
            organizer_id=organizer_id,
            title=data.get('title'),
            description=data.get('description'),
            location=data.get('location'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            capacity=data.get('capacity'),
            status=data.get('status', 'open')
        )

        return self.repository.create(workshop)

    def update(self, workshop_id, data, user_id, role):
        workshop, error = self.get_by_id_for_user(
            workshop_id=workshop_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Chỉ Expert là owner của workshop
        if role != 'admin':
            if str(workshop.organizer_id) != str(user_id):
                return None, 'forbidden'

        if 'title' in data:
            workshop.title = data.get('title')

        if 'description' in data:
            workshop.description = data.get('description')

        if 'location' in data:
            workshop.location = data.get('location')

        if 'start_time' in data:
            workshop.start_time = data.get('start_time')

        if 'end_time' in data:
            workshop.end_time = data.get('end_time')

        if 'capacity' in data:
            workshop.capacity = data.get('capacity')

        if 'status' in data:
            workshop.status = data.get('status')

        return self.repository.update(workshop), None

    def delete(self, workshop_id, user_id, role):
        workshop, error = self.get_by_id_for_user(
            workshop_id=workshop_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        # Chỉ Expert owner hoặc Admin được xóa
        if role != 'admin':
            if str(workshop.organizer_id) != str(user_id):
                return False, 'forbidden'

        self.repository.delete(workshop)

        return True, None