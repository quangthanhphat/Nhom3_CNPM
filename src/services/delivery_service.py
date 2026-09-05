from infrastructure.models.generated_models import Deliveries
from infrastructure.repositories.delivery_repository import DeliveryRepository


class DeliveryService:
    def __init__(self):
        self.repository = DeliveryRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, delivery_id):
        return self.repository.get_by_id(delivery_id)

    def create(self, data):
        delivery = Deliveries(
            order_id=data.get('order_id'),
            delivery_partner_id=data.get('delivery_partner_id'),
            delivery_type=data.get('delivery_type'),
            pickup_address=data.get('pickup_address'),
            destination_address=data.get('destination_address'),
            status=data.get('status', 'pending'),
            external_delivery_reference=data.get(
                'external_delivery_reference'
            )
        )

        return self.repository.create(delivery)

    def update(self, delivery_id, data):
        delivery = self.repository.get_by_id(delivery_id)

        if not delivery:
            return None

        delivery.order_id = data.get(
            'order_id',
            delivery.order_id
        )
        delivery.delivery_partner_id = data.get(
            'delivery_partner_id',
            delivery.delivery_partner_id
        )
        delivery.delivery_type = data.get(
            'delivery_type',
            delivery.delivery_type
        )
        delivery.pickup_address = data.get(
            'pickup_address',
            delivery.pickup_address
        )
        delivery.destination_address = data.get(
            'destination_address',
            delivery.destination_address
        )
        delivery.status = data.get(
            'status',
            delivery.status
        )
        delivery.external_delivery_reference = data.get(
            'external_delivery_reference',
            delivery.external_delivery_reference
        )

        return self.repository.update(delivery)

    def delete(self, delivery_id):
        delivery = self.repository.get_by_id(delivery_id)

        if not delivery:
            return False

        self.repository.delete(delivery)

        return True