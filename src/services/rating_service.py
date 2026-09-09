from infrastructure.models.generated_models import Ratings
from infrastructure.repositories.rating_repository import RatingRepository


class RatingService:

    def __init__(self):
        self.repository = RatingRepository()

    # =========================
    # GET ALL
    # =========================

    def list_all(self):
        return self.repository.list_all()

    # =========================
    # GET RATINGS BY USER
    # =========================

    def list_for_user(self, user_id, role):

        ratings = self.repository.list_all()

        if role == 'admin':
            return ratings

        return [
            rating
            for rating in ratings
            if str(rating.user_id) == str(user_id)
        ]

    # =========================
    # GET RATINGS FOR POST
    # =========================

    def list_for_post(self, post_id):

        ratings = self.repository.list_all()

        return [
            rating
            for rating in ratings
            if rating.target_type == 'post'
            and str(rating.target_id) == str(post_id)
        ]

    # =========================
    # GET USER RATING FOR POST
    # =========================

    def get_user_rating_for_post(self, post_id, user_id):

        ratings = self.list_for_post(post_id)

        for rating in ratings:
            if str(rating.user_id) == str(user_id):
                return rating

        return None

    # =========================
    # GET RATING BY ID
    # =========================

    def get_by_id(self, rating_id):
        return self.repository.get_by_id(rating_id)

    # =========================
    # GET RATING BY ID FOR USER
    # =========================

    def get_by_id_for_user(self, rating_id, user_id, role):

        rating = self.repository.get_by_id(rating_id)

        if not rating:
            return None, 'not_found'

        if role == 'admin':
            return rating, None

        if str(rating.user_id) != str(user_id):
            return None, 'forbidden'

        return rating, None

    # =========================
    # CREATE / UPDATE RATING
    # =========================

    def create(self, user_id, data):

        target_type = data.get('target_type')
        target_id = data.get('target_id')
        rating_value = data.get('rating')
        review = data.get('review')

        # ---------------------------------
        # Check existing rating
        # ---------------------------------

        existing_rating = None

        if target_type == 'post' and target_id:

            existing_rating = self.get_user_rating_for_post(
                post_id=target_id,
                user_id=user_id
            )

        # ---------------------------------
        # Already rated
        # -> update existing rating
        # ---------------------------------

        if existing_rating:

            existing_rating.rating = rating_value

            if 'review' in data:
                existing_rating.review = review

            return self.repository.update(existing_rating)

        # ---------------------------------
        # First rating
        # -> create new rating
        # ---------------------------------

        rating = Ratings(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            rating=rating_value,
            review=review
        )

        return self.repository.create(rating)

    # =========================
    # UPDATE RATING
    # =========================

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

        if 'review' in data:
            rating.review = data.get('review')

        return self.repository.update(rating), None

    # =========================
    # DELETE RATING
    # =========================

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