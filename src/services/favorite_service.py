from infrastructure.models.generated_models import Favorites
from infrastructure.repositories.favorite_repository import FavoriteRepository


class FavoriteService:

    def __init__(self):
        self.repository = FavoriteRepository()

    def list_for_user(self, user_id, role):
        favorites = self.repository.list_all()

        if role == 'admin':
            return favorites

        return [
            favorite
            for favorite in favorites
            if str(favorite.user_id) == str(user_id)
        ]

    def get_by_id_for_user(self, favorite_id, user_id, role):
        favorite = self.repository.get_by_id(favorite_id)

        if not favorite:
            return None, 'not_found'

        if role == 'admin':
            return favorite, None

        if str(favorite.user_id) != str(user_id):
            return None, 'forbidden'

        return favorite, None

    def create(self, user_id, data):
        favorite = Favorites(
            user_id=user_id,
            target_type=data.get('target_type'),
            target_id=data.get('target_id')
        )

        return self.repository.create(favorite)

    def delete(self, favorite_id, user_id, role):
        favorite, error = self.get_by_id_for_user(
            favorite_id=favorite_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(favorite)

        return True, None