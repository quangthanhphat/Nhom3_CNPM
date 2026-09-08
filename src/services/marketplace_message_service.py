from infrastructure.models.generated_models import MarketplaceMessages
from infrastructure.repositories.marketplace_message_repository import (
    MarketplaceMessageRepository
)
from infrastructure.repositories.marketplace_listing_repository import (
    MarketplaceListingRepository
)


class MarketplaceMessageService:

    def __init__(self):
        self.repository = MarketplaceMessageRepository()
        self.listing_repository = MarketplaceListingRepository()

    def list_for_user(self, user_id, role):
        messages = self.repository.list_all()

        if role == 'admin':
            return messages

        result = []

        for message in messages:
            if str(message.sender_id) == str(user_id):
                result.append(message)
                continue

            if str(message.receiver_id) == str(user_id):
                result.append(message)

        return result

    def get_by_id_for_user(self, message_id, user_id, role):
        message = self.repository.get_by_id(message_id)

        if not message:
            return None, 'not_found'

        if role == 'admin':
            return message, None

        if (
            str(message.sender_id) == str(user_id)
            or str(message.receiver_id) == str(user_id)
        ):
            return message, None

        return None, 'forbidden'

    def create(self, sender_id, data):
        listing_id = data.get('listing_id')
        receiver_id = data.get('receiver_id')

        listing = self.listing_repository.get_by_id(
            listing_id
        )

        if not listing:
            return None, 'listing_not_found'

        if str(sender_id) == str(receiver_id):
            return None, 'invalid_receiver'

        # Chỉ buyer/seller liên quan đến listing được nhắn
        seller_id = str(listing.seller_id)

        if (
            str(sender_id) != seller_id
            and str(receiver_id) != seller_id
        ):
            return None, 'forbidden'

        message = MarketplaceMessages(
            listing_id=listing_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=data.get('content')
        )

        return self.repository.create(message), None

    def delete(self, message_id, user_id, role):
        message, error = self.get_by_id_for_user(
            message_id=message_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(message)

        return True, None