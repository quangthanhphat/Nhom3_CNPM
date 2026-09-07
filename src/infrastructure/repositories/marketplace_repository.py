from domain.models.marketplace_model import Product
from infrastructure.databases.factory_database import FactoryDatabase as db_factory

class MarketplaceRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def get_all(self, category=None):
        query = self.session.query(Product)
        if category:
            query = query.filter(Product.category == category)
        return query.all()

    def get_by_id(self, product_id):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def create(self, product_data):
        new_product = Product(**product_data)
        self.session.add(new_product)
        self.session.commit()
        return new_product

    def update_status(self, product_id, status):
        product = self.get_by_id(product_id)
        if product:
            product.status = status
            self.session.commit()
        return product