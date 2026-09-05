from infrastructure.models.generated_models import Payments
from infrastructure.repositories.payment_repository import PaymentRepository


class PaymentService:
    def __init__(self):
        self.repository = PaymentRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, payment_id):
        return self.repository.get_by_id(payment_id)

    def create(self, data):
        payment = Payments(
            order_id=data.get('order_id'),
            amount=data.get('amount'),
            transaction_reference=data.get('transaction_reference'),
            status=data.get('status', 'pending'),
            paid_at=data.get('paid_at')
        )

        return self.repository.create(payment)

    def update(self, payment_id, data):
        payment = self.repository.get_by_id(payment_id)

        if not payment:
            return None

        payment.order_id = data.get(
            'order_id',
            payment.order_id
        )
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

        return self.repository.update(payment)

    def delete(self, payment_id):
        payment = self.repository.get_by_id(payment_id)

        if not payment:
            return False

        self.repository.delete(payment)

        return True