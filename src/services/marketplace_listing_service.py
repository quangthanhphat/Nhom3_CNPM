from infrastructure.models.generated_models import MarketplaceListings
from infrastructure.repositories.marketplace_listing_repository import (
    MarketplaceListingRepository
)


class MarketplaceListingService:

    def __init__(self):
        self.repository = MarketplaceListingRepository()

    def list_for_user(self, user_id, role):
        listings = self.repository.list_all()

        # Marketplace cho phép các role này xem listing
        if role in [
            'customer',
            'film_lab_owner',
            'photography_expert',
            'delivery_partner',
            'admin'
        ]:
            return listings

        return []

    def get_by_id_for_user(self, listing_id, user_id, role):
        listing = self.repository.get_by_id(listing_id)

        if not listing:
            return None, 'not_found'

        if role in [
            'customer',
            'film_lab_owner',
            'photography_expert',
            'delivery_partner',
            'admin'
        ]:
            return listing, None

        return None, 'forbidden'

    def create(self, seller_id, data):
        listing = MarketplaceListings(
            seller_id=seller_id,
            category=data.get('category'),
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            quantity=data.get('quantity', 1),
            status=data.get('status', 'active')
        )

        return self.repository.create(listing)

    def update(self, listing_id, data, user_id, role):
        listing = self.repository.get_by_id(listing_id)

        if not listing:
            return None, 'not_found'

        # Admin được sửa tất cả
        if role != 'admin':
            if str(listing.seller_id) != str(user_id):
                return None, 'forbidden'

        if 'category' in data:
            listing.category = data.get('category')

        if 'title' in data:
            listing.title = data.get('title')

        if 'description' in data:
            listing.description = data.get('description')

        if 'price' in data:
            listing.price = data.get('price')

        if 'quantity' in data:
            listing.quantity = data.get('quantity')

        if 'status' in data:
            listing.status = data.get('status')

        return self.repository.update(listing), None

    def delete(self, listing_id, user_id, role):
        listing = self.repository.get_by_id(listing_id)

        if not listing:
            return False, 'not_found'

        # Admin được xóa tất cả
        if role != 'admin':
            if str(listing.seller_id) != str(user_id):
                return False, 'forbidden'

        self.repository.delete(listing)

        return True, None