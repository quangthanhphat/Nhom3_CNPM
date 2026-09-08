from infrastructure.models.generated_models import Ratings
from infrastructure.repositories.rating_repository import RatingRepository


class RatingService:

    def __init__(self):
        self.repository = RatingRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        ratings = self.repository.list_all()

        if role == 'admin':
            return ratings

        return [
            rating
            for rating in ratings
            if str(rating.user_id) == str(user_id)
        ]

    def get_by_id_for_user(self, rating_id, user_id, role):
        rating = self.repository.get_by_id(rating_id)

        if not rating:
            return None, 'not_found'

        if role == 'admin':
            return rating, None

        if str(rating.user_id) != str(user_id):
            return None, 'forbidden'

        return rating, None

    def create(self, user_id, data):
        rating = Ratings(
            user_id=user_id,
            order_id=data.get('order_id'),
            rating=data.get('rating'),
            review_text=data.get('review_text')
        )

        return self.repository.create(rating)

    def update(self, rating_id, data, user_id, role):
        rating, error = self.get_by_id_for_user(
            rating_id=rating_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        if 'rating' in data:
            rating.rating = data.get('rating')

        if 'review_text' in data:
            rating.review_text = data.get('review_text')

        return self.repository.update(rating), None

    def delete(self, rating_id, user_id, role):
        rating, error = self.get_by_id_for_user(
            rating_id=rating_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(rating)

        return True, None