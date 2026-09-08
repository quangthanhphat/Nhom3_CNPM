from infrastructure.models.generated_models import Services
from infrastructure.repositories.service_repository import ServiceRepository


class ServiceService:
    def __init__(self):
        self.repository = ServiceRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, service_id):
        return self.repository.get_by_id(service_id)

    def create(self, data):
        service = Services(
            film_lab_id=data.get('film_lab_id'),
            category_id=data.get('category_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            turnaround_time_min=data.get('turnaround_time_min'),
            turnaround_time_max=data.get('turnaround_time_max'),
            processing_capacity=data.get('processing_capacity'),
            supported_film_formats=data.get(
                'supported_film_formats'
            ),
            processing_options=data.get(
                'processing_options'
            ),
            scanning_quality=data.get(
                'scanning_quality'
            ),
            printing_options=data.get(
                'printing_options'
            ),
            specialized_techniques=data.get(
                'specialized_techniques'
            )
        )

        return self.repository.create(service)

    def update(
        self,
        service_id,
        data,
        user_id=None,
        is_admin=False
    ):
        service = self.repository.get_by_id(service_id)

        if not service:
            return None, 'not_found'

        # Admin được quản lý tất cả service.
        # Owner chỉ được quản lý service thuộc Film Lab của mình.
        if not is_admin:
            if not service.film_lab:
                return None, 'forbidden'

            if str(service.film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

        service.film_lab_id = data.get(
            'film_lab_id',
            service.film_lab_id
        )
        service.category_id = data.get(
            'category_id',
            service.category_id
        )
        service.name = data.get(
            'name',
            service.name
        )
        service.description = data.get(
            'description',
            service.description
        )
        service.price = data.get(
            'price',
            service.price
        )
        service.turnaround_time_min = data.get(
            'turnaround_time_min',
            service.turnaround_time_min
        )
        service.turnaround_time_max = data.get(
            'turnaround_time_max',
            service.turnaround_time_max
        )
        service.processing_capacity = data.get(
            'processing_capacity',
            service.processing_capacity
        )
        service.supported_film_formats = data.get(
            'supported_film_formats',
            service.supported_film_formats
        )
        service.processing_options = data.get(
            'processing_options',
            service.processing_options
        )
        service.scanning_quality = data.get(
            'scanning_quality',
            service.scanning_quality
        )
        service.printing_options = data.get(
            'printing_options',
            service.printing_options
        )
        service.specialized_techniques = data.get(
            'specialized_techniques',
            service.specialized_techniques
        )

        return self.repository.update(service), None

    def delete(
        self,
        service_id,
        user_id=None,
        is_admin=False
    ):
        service = self.repository.get_by_id(service_id)

        if not service:
            return False, 'not_found'

        # Admin được xóa tất cả service.
        # Owner chỉ được xóa service thuộc Film Lab của mình.
        if not is_admin:
            if not service.film_lab:
                return False, 'forbidden'

            if str(service.film_lab.owner_id) != str(user_id):
                return False, 'forbidden'

        self.repository.delete(service)

        return True, None