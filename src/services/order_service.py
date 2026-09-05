from infrastructure.models.generated_models import Orders
from infrastructure.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self):
        self.repository = OrderRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, order_id):
        return self.repository.get_by_id(order_id)

    def create(self, customer_id, data):
        order = Orders(
            customer_id=customer_id,
            film_lab_id=data.get('film_lab_id'),
            service_id=data.get('service_id'),
            film_type_id=data.get('film_type_id'),
            processing_options=data.get('processing_options'),
            scanning_quality=data.get('scanning_quality'),
            printing_requirements=data.get('printing_requirements'),
            additional_requests=data.get('additional_requests'),
            total_amount=data.get('total_amount'),
            notes=data.get('notes')
        )

        return self.repository.create(order)

    def update(self, order_id, data):
        order = self.repository.get_by_id(order_id)

        if not order:
            return None

        order.film_lab_id = data.get('film_lab_id', order.film_lab_id)
        order.service_id = data.get('service_id', order.service_id)
        order.film_type_id = data.get('film_type_id', order.film_type_id)
        order.processing_options = data.get(
            'processing_options',
            order.processing_options
        )
        order.scanning_quality = data.get(
            'scanning_quality',
            order.scanning_quality
        )
        order.printing_requirements = data.get(
            'printing_requirements',
            order.printing_requirements
        )
        order.additional_requests = data.get(
            'additional_requests',
            order.additional_requests
        )
        order.total_amount = data.get(
            'total_amount',
            order.total_amount
        )
        order.notes = data.get('notes', order.notes)
        order.status = data.get('status', order.status)

        return self.repository.update(order)

    def delete(self, order_id):
        order = self.repository.get_by_id(order_id)

        if not order:
            return False

        self.repository.delete(order)

        return True