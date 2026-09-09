from infrastructure.models.generated_models import Ratings
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class RatingRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    # =========================
    # GET ALL RATINGS
    # =========================

    def list_all(self):
        return self.session.query(Ratings).all()

    # =========================
    # GET RATINGS FOR POST
    # =========================

    def list_for_post(self, post_id):
        return self.session.query(Ratings).filter(
            Ratings.target_type == 'post',
            Ratings.target_id == post_id
        ).all()

    # =========================
    # GET USER RATING FOR POST
    # =========================

    def get_user_rating_for_post(self, user_id, post_id):
        return self.session.query(Ratings).filter(
            Ratings.user_id == user_id,
            Ratings.target_type == 'post',
            Ratings.target_id == post_id
        ).first()

    # =========================
    # GET BY ID
    # =========================

    def get_by_id(self, rating_id):
        return self.session.query(Ratings).filter(
            Ratings.id == rating_id
        ).first()

    # =========================
    # CREATE
    # =========================

    def create(self, rating):
        self.session.add(rating)
        self.session.commit()
        self.session.refresh(rating)

        return rating

    # =========================
    # UPDATE
    # =========================

    def update(self, rating):
        self.session.commit()
        self.session.refresh(rating)

        return rating

    # =========================
    # DELETE
    # =========================

    def delete(self, rating):
        self.session.delete(rating)
        self.session.commit()