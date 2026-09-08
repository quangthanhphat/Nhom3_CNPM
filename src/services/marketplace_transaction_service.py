from infrastructure.models.generated_models import MarketplaceTransactions
from infrastructure.repositories.marketplace_transaction_repository import (
    MarketplaceTransactionRepository
)
from infrastructure.repositories.marketplace_listing_repository import (
    MarketplaceListingRepository
)


class MarketplaceTransactionService:

    def __init__(self):
        self.repository = MarketplaceTransactionRepository()
        self.listing_repository = MarketplaceListingRepository()

    def list_for_user(self, user_id, role):
        transactions = self.repository.list_all()

        if role == 'admin':
            return transactions

        if role in [
            'customer',
            'film_lab_owner',
            'photography_expert'
        ]:
            result = []

            for transaction in transactions:
                if str(transaction.buyer_id) == str(user_id):
                    result.append(transaction)
                    continue

                listing = self.listing_repository.get_by_id(
                    transaction.listing_id
                )

                if (
                    listing
                    and str(listing.seller_id) == str(user_id)
                ):
                    result.append(transaction)

            return result

        return []

    def get_by_id_for_user(self, transaction_id, user_id, role):
        transaction = self.repository.get_by_id(
            transaction_id
        )

        if not transaction:
            return None, 'not_found'

        if role == 'admin':
            return transaction, None

        if role in [
            'customer',
            'film_lab_owner',
            'photography_expert'
        ]:
            if str(transaction.buyer_id) == str(user_id):
                return transaction, None

            listing = self.listing_repository.get_by_id(
                transaction.listing_id
            )

            if (
                listing
                and str(listing.seller_id) == str(user_id)
            ):
                return transaction, None

        return None, 'forbidden'

    def create(self, buyer_id, data):
        listing_id = data.get('listing_id')
        quantity = data.get('quantity', 1)

        if quantity is None or quantity <= 0:
            return None, 'invalid_quantity'

        listing = self.listing_repository.get_by_id(
            listing_id
        )

        if not listing:
            return None, 'listing_not_found'

        if str(listing.seller_id) == str(buyer_id):
            return None, 'own_listing'

        if listing.status == 'sold_out':
            return None, 'sold_out'

        if listing.quantity is None:
            return None, 'invalid_quantity'

        if quantity > listing.quantity:
            return None, 'insufficient_quantity'

        total_amount = listing.price * quantity

        transaction = MarketplaceTransactions(
            listing_id=listing.id,
            buyer_id=buyer_id,
            quantity=quantity,
            total_amount=total_amount,
            status='completed'
        )

        listing.quantity -= quantity

        if listing.quantity == 0:
            listing.status = 'sold_out'

        self.listing_repository.update(listing)

        return self.repository.create(transaction), None

    def delete(self, transaction_id, user_id, role):
        transaction, error = self.get_by_id_for_user(
            transaction_id=transaction_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(transaction)

        return True, None