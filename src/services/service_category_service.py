from infrastructure.models.generated_models import ServiceCategories
from infrastructure.repositories.service_category_repository import ServiceCategoryRepository


class ServiceCategoryService:
    def __init__(self):
        self.repository = ServiceCategoryRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, category_id):
        return self.repository.get_by_id(category_id)

    def create(self, data):
        category = ServiceCategories(
            name=data.get('name'),
            description=data.get('description')
        )

        return self.repository.create(category)

    def update(self, category_id, data):
        category = self.repository.get_by_id(category_id)

        if not category:
            return None

        category.name = data.get('name', category.name)
        category.description = data.get(
            'description',
            category.description
        )

        return self.repository.update(category)

    def delete(self, category_id):
        category = self.repository.get_by_id(category_id)

        if not category:
            return False

        self.repository.delete(category)

        return True