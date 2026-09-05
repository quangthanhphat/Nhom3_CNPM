from infrastructure.models.generated_models import ServiceCategories
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class ServiceCategoryRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(ServiceCategories).all()

    def get_by_id(self, category_id):
        return self.session.query(ServiceCategories).filter(
            ServiceCategories.id == category_id
        ).first()

    def create(self, category):
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def update(self, category):
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category):
        self.session.delete(category)
        self.session.commit()