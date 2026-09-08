from infrastructure.models.generated_models import Orders
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class OrderService:
    def __init__(self):
        self.repository = OrderRepository()
        self.film_lab_repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        orders = self.repository.list_all()

        # Admin được xem tất cả order
        if role == 'admin':
            return orders

        # Customer chỉ xem order của mình
        if role == 'customer':
            return [
                order
                for order in orders
                if str(order.customer_id) == str(user_id)
            ]

        # Film Lab Owner chỉ xem order thuộc lab của mình
        if role == 'film_lab_owner':
            result = []

            for order in orders:
                film_lab = self.film_lab_repository.get_by_id(
                    order.film_lab_id
                )

                if (
                    film_lab
                    and str(film_lab.owner_id) == str(user_id)
                ):
                    result.append(order)

            return result

        return []

    def get_by_id(self, order_id):
        return self.repository.get_by_id(order_id)

    def get_by_id_for_user(self, order_id, user_id, role):
        order = self.repository.get_by_id(order_id)

        if not order:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return order, None

        # Customer chỉ xem order của mình
        if role == 'customer':
            if str(order.customer_id) != str(user_id):
                return None, 'forbidden'

            return order, None

        # Film Lab Owner chỉ xem order thuộc lab của mình
        if role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

            return order, None

        return None, 'forbidden'

    def create(self, customer_id, data):
        order = Orders(
            customer_id=customer_id,
            film_lab_id=data.get('film_lab_id'),
            service_id=data.get('service_id'),
            film_type_id=data.get('film_type_id'),
            processing_options=data.get('processing_options'),
            scanning_quality=data.get('scanning_quality'),
            printing_requirements=data.get(
                'printing_requirements'
            ),
            additional_requests=data.get(
                'additional_requests'
            ),
            total_amount=data.get('total_amount'),
            notes=data.get('notes')
        )

        return self.repository.create(order)

    def update(
        self,
        order_id,
        data,
        user_id,
        role
    ):
        order, error = self.get_by_id_for_user(
            order_id=order_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Không cho thay đổi customer_id
        # vì customer_id phải là người tạo order.

        order.film_lab_id = data.get(
            'film_lab_id',
            order.film_lab_id
        )

        order.service_id = data.get(
            'service_id',
            order.service_id
        )

        order.film_type_id = data.get(
            'film_type_id',
            order.film_type_id
        )

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

        order.notes = data.get(
            'notes',
            order.notes
        )

        order.status = data.get(
            'status',
            order.status
        )

        return self.repository.update(order), None

    def delete(
        self,
        order_id,
        user_id,
        role
    ):
        order, error = self.get_by_id_for_user(
            order_id=order_id,
            user_id=user_id,
            role=role
        )

        if error:
            if error == 'not_found':
                return False, 'not_found'

            return False, 'forbidden'

        self.repository.delete(order)

        return True, None