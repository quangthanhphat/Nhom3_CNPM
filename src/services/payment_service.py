from datetime import datetime, timezone

from infrastructure.models.generated_models import Payments
from infrastructure.repositories.payment_repository import PaymentRepository
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.film_lab_repository import FilmLabRepository


class PaymentService:
    def __init__(self):
        self.repository = PaymentRepository()
        self.order_repository = OrderRepository()
        self.film_lab_repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        payments = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return payments

        result = []

        for payment in payments:
            order = self.order_repository.get_by_id(
                payment.order_id
            )

            if not order:
                continue

            # Customer chỉ xem payment của order mình
            if role == 'customer':
                if str(order.customer_id) == str(user_id):
                    result.append(payment)

            # Film Lab Owner chỉ xem payment
            # của order thuộc lab của mình
            elif role == 'film_lab_owner':
                film_lab = self.film_lab_repository.get_by_id(
                    order.film_lab_id
                )

                if (
                    film_lab
                    and str(film_lab.owner_id) == str(user_id)
                ):
                    result.append(payment)

        return result

    def get_by_id(self, payment_id):
        return self.repository.get_by_id(payment_id)

    def get_by_id_for_user(self, payment_id, user_id, role):
        payment = self.repository.get_by_id(payment_id)

        if not payment:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return payment, None

        order = self.order_repository.get_by_id(
            payment.order_id
        )

        if not order:
            return None, 'not_found'

        # Customer chỉ xem payment của order mình
        if role == 'customer':
            if str(order.customer_id) != str(user_id):
                return None, 'forbidden'

            return payment, None

        # Film Lab Owner chỉ xem payment
        # của order thuộc lab mình
        if role == 'film_lab_owner':
            film_lab = self.film_lab_repository.get_by_id(
                order.film_lab_id
            )

            if not film_lab:
                return None, 'forbidden'

            if str(film_lab.owner_id) != str(user_id):
                return None, 'forbidden'

            return payment, None

        return None, 'forbidden'

    def create(self, data, user_id, role):
        order_id = data.get('order_id')

        order = self.order_repository.get_by_id(order_id)

        if not order:
            return None, 'order_not_found'

        # ==========================================
        # CHECK PERMISSION
        # ==========================================

        if role == 'admin':
            pass

        elif role == 'customer':
            if str(order.customer_id) != str(user_id):
                return None, 'forbidden'

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

        # ==========================================
        # PAYMENT FLOW
        # ==========================================

        current_status = (
            str(order.status).lower()
            if order.status
            else ''
        )

        # Chỉ order đã được Owner accept mới được thanh toán
        if current_status != 'confirmed':
            return None, 'order_not_ready_for_payment'

        # ==========================================
        # CREATE PAYMENT
        # ==========================================

        payment_status = data.get(
            'status',
            'pending'
        )

        payment = Payments(
            order_id=order_id,
            amount=data.get('amount'),
            transaction_reference=data.get(
                'transaction_reference'
            ),
            status=payment_status,
            paid_at=data.get('paid_at')
        )

        # ==========================================
        # DEMO PAYMENT SUCCESS
        # ==========================================
        #
        # Nếu payment có status = completed
        # thì coi như khách đã thanh toán thành công.
        #
        # Sau đó Order tự động chuyển:
        #
        # confirmed -> processing
        #

        if str(payment_status).lower() == 'completed':
            if not payment.paid_at:
                payment.paid_at = datetime.now(timezone.utc)

        payment = self.repository.create(payment)

        # ==========================================
        # UPDATE ORDER STATUS
        # ==========================================

        if str(payment.status).lower() == 'completed':
            order.status = 'processing'

            self.order_repository.update(order)

        return payment, None

    def update(
        self,
        payment_id,
        data,
        user_id,
        role
    ):
        payment, error = self.get_by_id_for_user(
            payment_id=payment_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Nếu đổi order_id thì phải kiểm tra
        # order mới cũng thuộc quyền của user.
        new_order_id = data.get('order_id')

        if new_order_id:
            new_order = self.order_repository.get_by_id(
                new_order_id
            )

            if not new_order:
                return None, 'order_not_found'

            if role == 'customer':
                if str(new_order.customer_id) != str(user_id):
                    return None, 'forbidden'

            elif role == 'film_lab_owner':
                film_lab = self.film_lab_repository.get_by_id(
                    new_order.film_lab_id
                )

                if (
                    not film_lab
                    or str(film_lab.owner_id) != str(user_id)
                ):
                    return None, 'forbidden'

            payment.order_id = new_order_id

        payment.amount = data.get(
            'amount',
            payment.amount
        )

        payment.transaction_reference = data.get(
            'transaction_reference',
            payment.transaction_reference
        )

        payment.status = data.get(
            'status',
            payment.status
        )

        payment.paid_at = data.get(
            'paid_at',
            payment.paid_at
        )

        return self.repository.update(payment), None

    def delete(
        self,
        payment_id,
        user_id,
        role
    ):
        payment, error = self.get_by_id_for_user(
            payment_id=payment_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(payment)

        return True, None