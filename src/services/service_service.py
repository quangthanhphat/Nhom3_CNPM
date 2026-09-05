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
            turnaround_time=data.get('turnaround_time'),
            processing_capacity=data.get('processing_capacity'),
            supported_film_formats=data.get('supported_film_formats'),
            processing_options=data.get('processing_options'),
            scanning_quality=data.get('scanning_quality'),
            printing_options=data.get('printing_options'),
            specialized_techniques=data.get('specialized_techniques')
        )

        return self.repository.create(service)

    def update(self, service_id, data):
        service = self.repository.get_by_id(service_id)

        if not service:
            return None

        service.film_lab_id = data.get(
            'film_lab_id',
            service.film_lab_id
        )
        service.category_id = data.get(
            'category_id',
            service.category_id
        )
        service.name = data.get('name', service.name)
        service.description = data.get(
            'description',
            service.description
        )
        service.price = data.get('price', service.price)
        service.turnaround_time = data.get(
            'turnaround_time',
            service.turnaround_time
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

        return self.repository.update(service)

    def delete(self, service_id):
        service = self.repository.get_by_id(service_id)

        if not service:
            return False

        self.repository.delete(service)

        return True