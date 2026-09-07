from infrastructure.repositories.marketplace_repository import MarketplaceRepository

class MarketplaceService:
    def __init__(self):
        self.repository = MarketplaceRepository()

    def list_products(self, category=None):
        products = self.repository.get_all(category)
        return [p.to_dict() for p in products]

    def get_product(self, product_id):
        product = self.repository.get_by_id(product_id)
        return product.to_dict() if product else None

    def add_product(self, seller_id, data):
        product_data = data.copy() if data else {}
        product_data['seller_id'] = seller_id
        product = self.repository.create(product_data)
        return product.to_dict()