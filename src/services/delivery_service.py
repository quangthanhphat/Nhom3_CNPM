from infrastructure.models.generated_models import Deliveries
from infrastructure.repositories.delivery_repository import DeliveryRepository
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class DeliveryService:
    def __init__(self):
        self.repository = DeliveryRepository()
        self.order_repository = OrderRepository()
        self.film_lab_repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        deliveries = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return deliveries

        result = []

        for delivery in deliveries:
            order = self.order_repository.get_by_id(
                delivery.order_id
            )

            if not order:
                continue

            # Customer chỉ xem delivery của order mình
            if role == 'customer':
                if str(order.customer_id) == str(user_id):
                    result.append(delivery)

            # Film Lab Owner chỉ xem delivery
            # của order thuộc lab mình
            elif role == 'film_lab_owner':
                film_lab = self.film_lab_repository.get_by_id(
                    order.film_lab_id
                )

                if (
                    film_lab
                    and str(film_lab.owner_id) == str(user_id)
                ):
                    result.append(delivery)

            # Delivery Partner chỉ xem delivery được giao cho mình
            elif role == 'delivery_partner':
                if (
                    delivery.delivery_partner_id
                    and str(delivery.delivery_partner_id)
                    == str(user_id)
                ):
                    result.append(delivery)

        return result

    def get_by_id(self, delivery_id):
        return self.repository.get_by_id(delivery_id)

    def get_by_id_for_user(self, delivery_id, user_id, role):
        delivery = self.repository.get_by_id(delivery_id)

        if not delivery:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return delivery, None

        # Delivery Partner chỉ xem delivery được giao cho mình
        if role == 'delivery_partner':
            if (
                delivery.delivery_partner_id
                and str(delivery.delivery_partner_id)
                == str(user_id)
            ):
                return delivery, None

            return None, 'forbidden'

        order = self.order_repository.get_by_id(
            delivery.order_id
        )

        if not order:
            return None, 'not_found'

        # Customer chỉ xem delivery của order mình
        if role == 'customer':
            if str(order.customer_id) != str(user_id):
                return None, 'forbidden'

            return delivery, None

        # Film Lab Owner chỉ xem delivery
        # của order thuộc lab mình
        if role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

            return delivery, None

        return None, 'forbidden'

    def create(self, data, user_id, role):
        order_id = data.get('order_id')

        order = self.order_repository.get_by_id(order_id)

        if not order:
            return None, 'order_not_found'

        # Admin được tạo delivery cho mọi order
        if role == 'admin':
            pass

        # Film Lab Owner chỉ tạo delivery
        # cho order thuộc lab của mình
        elif role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

        else:
            return None, 'forbidden'

        delivery = Deliveries(
            order_id=order_id,
            delivery_partner_id=data.get(
                'delivery_partner_id'
            ),
            delivery_type=data.get('delivery_type'),
            pickup_address=data.get('pickup_address'),
            destination_address=data.get(
                'destination_address'
            ),
            status=data.get(
                'status',
                'pending'
            ),
            external_delivery_reference=data.get(
                'external_delivery_reference'
            )
        )

        return self.repository.create(delivery), None

    def update(
        self,
        delivery_id,
        data,
        user_id,
        role
    ):
        delivery, error = self.get_by_id_for_user(
            delivery_id=delivery_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Nếu đổi order_id thì phải kiểm tra
        # order mới có thuộc quyền quản lý hay không.
        new_order_id = data.get('order_id')

        if new_order_id:
            new_order = self.order_repository.get_by_id(
                new_order_id
            )

            if not new_order:
                return None, 'order_not_found'

            if role == 'film_lab_owner':
                film_lab = self.film_lab_repository.get_by_id(
                    new_order.film_lab_id
                )

                if (
                    not film_lab
                    or str(film_lab.owner_id) != str(user_id)
                ):
                    return None, 'forbidden'

            elif role == 'customer':
                if str(new_order.customer_id) != str(user_id):
                    return None, 'forbidden'

            elif role == 'delivery_partner':
                return None, 'forbidden'

            delivery.order_id = new_order_id

        # Delivery Partner không được tự chuyển delivery
        # sang Delivery Partner khác.
        if role == 'delivery_partner':
            if 'delivery_partner_id' in data:
                new_partner_id = data.get(
                    'delivery_partner_id'
                )

                if (
                    new_partner_id
                    and str(new_partner_id) != str(user_id)
                ):
                    return None, 'forbidden'

        else:
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

        return self.repository.update(delivery), None

    def delete(
        self,
        delivery_id,
        user_id,
        role
    ):
        delivery, error = self.get_by_id_for_user(
            delivery_id=delivery_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        # Delivery Partner không được xóa delivery.
        if role == 'delivery_partner':
            return False, 'forbidden'

        self.repository.delete(delivery)

        return True, None