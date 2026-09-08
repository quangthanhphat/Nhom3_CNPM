from infrastructure.models.generated_models import TransactionFees
from infrastructure.repositories.transaction_fee_repository import (
    TransactionFeeRepository
)


class TransactionFeeService:

    def __init__(self):
        self.repository = TransactionFeeRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, fee_id):
        return self.repository.get_by_id(fee_id)

    def create(self, data):
        fee = TransactionFees(
            transaction_id=data.get('transaction_id'),
            fee_amount=data.get('fee_amount')
        )

        return self.repository.create(fee)

    def update(self, fee_id, data):
        fee = self.repository.get_by_id(fee_id)

        if not fee:
            return None

        if 'transaction_id' in data:
            fee.transaction_id = data.get('transaction_id')

        if 'fee_amount' in data:
            fee.fee_amount = data.get('fee_amount')

        return self.repository.update(fee)

    def delete(self, fee_id):
        fee = self.repository.get_by_id(fee_id)

        if not fee:
            return False

        self.repository.delete(fee)

        return True