from infrastructure.models.generated_models import Orders
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class OrderService:
    def __init__(self):
        self.repository = OrderRepository()
        self.film_lab_repository = FilmLabRepository()

    # =========================================================
    # ORDER STATUS FLOW
    # =========================================================

    VALID_STATUSES = [
        'pending',
        'confirmed',
        'processing',
        'start',
        'developing',
        'scanning',
        'printing',
        'quality_check',
        'completed',
        'ready_for_pickup',
        'delivering',
        'done',
        'cancelled',
    ]

    STATUS_TRANSITIONS = {
        'pending': [
            'confirmed',
            'cancelled',
        ],

        'confirmed': [
            'processing',
            'cancelled',
        ],

        'processing': [
            'start',
            'cancelled',
        ],

        'start': [
            'developing',
            'cancelled',
        ],

        'developing': [
            'scanning',
            'printing',
            'quality_check',
            'cancelled',
        ],

        'scanning': [
            'printing',
            'quality_check',
            'cancelled',
        ],

        'printing': [
            'quality_check',
            'cancelled',
        ],

        'quality_check': [
            'completed',
            'cancelled',
        ],

        'completed': [
            'ready_for_pickup',
            'delivering',
        ],

        'ready_for_pickup': [
            'done',
        ],

        'delivering': [
            'done',
        ],

        'done': [],

        'cancelled': [],
    }

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

    def get_by_id_for_user(
        self,
        order_id,
        user_id,
        role
    ):
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

    def create(
        self,
        customer_id,
        data
    ):
        delivery_type = data.get(
            'delivery_type',
            'pickup'
        )

        if delivery_type not in ['pickup', 'delivery']:
            delivery_type = 'pickup'

        quantity = data.get(
            'quantity',
            1
        )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        order = Orders(
            customer_id=customer_id,

            film_lab_id=data.get(
                'film_lab_id'
            ),

            service_id=data.get(
                'service_id'
            ),

            film_type_id=data.get(
                'film_type_id'
            ),

            quantity=quantity,

            processing_options=data.get(
                'processing_options'
            ),

            scanning_quality=data.get(
                'scanning_quality'
            ),

            printing_requirements=data.get(
                'printing_requirements'
            ),

            additional_requests=data.get(
                'additional_requests'
            ),

            delivery_type=delivery_type,

            total_amount=data.get(
                'total_amount'
            ),

            notes=data.get(
                'notes'
            ),

            # Customer vừa gửi yêu cầu.
            status='pending'
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

        # =====================================================
        # STATUS UPDATE
        # =====================================================

        if 'status' in data:
            requested_status = data.get('status')

            if requested_status is None:
                return None, 'invalid_status'

            requested_status = str(
                requested_status
            ).lower().strip()

            current_status = (
                str(order.status).lower().strip()
                if order.status
                else 'pending'
            )

            # Status không tồn tại
            if requested_status not in self.VALID_STATUSES:
                return None, 'invalid_status'

            # Không cho update lại cùng status
            if requested_status == current_status:
                return None, 'invalid_status_transition'

            # =================================================
            # CUSTOMER KHÔNG ĐƯỢC TỰ Ý ĐỔI STATUS
            # =================================================

            if role == 'customer':
                return None, 'forbidden'

            # =================================================
            # OWNER / ADMIN ĐƯỢC UPDATE THEO FLOW
            # =================================================

            allowed_next_statuses = self.STATUS_TRANSITIONS.get(
                current_status,
                []
            )

            if requested_status not in allowed_next_statuses:
                return None, 'invalid_status_transition'

            # =================================================
            # DELIVERY TYPE CHECK
            # =================================================

            if requested_status == 'delivering':
                if order.delivery_type != 'delivery':
                    return None, 'invalid_delivery_status'

            if requested_status == 'ready_for_pickup':
                if order.delivery_type != 'pickup':
                    return None, 'invalid_pickup_status'

            # =================================================
            # UPDATE STATUS
            # =================================================

            order.status = requested_status

        # =====================================================
        # OTHER ORDER DATA
        # =====================================================

        # Không cho thay đổi customer_id.
        # customer_id là người tạo order.

        if 'film_lab_id' in data:
            order.film_lab_id = data.get(
                'film_lab_id'
            )

        if 'service_id' in data:
            order.service_id = data.get(
                'service_id'
            )

        if 'film_type_id' in data:
            order.film_type_id = data.get(
                'film_type_id'
            )

        if 'quantity' in data:
            quantity = data.get('quantity')

            try:
                quantity = int(quantity)
            except (TypeError, ValueError):
                quantity = order.quantity

            if quantity < 1:
                quantity = order.quantity

            order.quantity = quantity

        if 'processing_options' in data:
            order.processing_options = data.get(
                'processing_options'
            )

        if 'scanning_quality' in data:
            order.scanning_quality = data.get(
                'scanning_quality'
            )

        if 'printing_requirements' in data:
            order.printing_requirements = data.get(
                'printing_requirements'
            )

        if 'additional_requests' in data:
            order.additional_requests = data.get(
                'additional_requests'
            )

        if 'delivery_type' in data:
            delivery_type = data.get(
                'delivery_type'
            )

            if delivery_type in ['pickup', 'delivery']:
                order.delivery_type = delivery_type

        if 'total_amount' in data:
            order.total_amount = data.get(
                'total_amount'
            )

        if 'notes' in data:
            order.notes = data.get(
                'notes'
            )

        return self.repository.update(
            order
        ), None

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