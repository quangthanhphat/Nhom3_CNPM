from infrastructure.models.generated_models import Comments, Users
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class CommentRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    # =========================================================
    # GET ALL COMMENTS + USER INFO
    # =========================================================

    def list_all(self):
        return (
            self.session.query(Comments, Users)
            .outerjoin(
                Users,
                Comments.author_id == Users.id
            )
            .order_by(
                Comments.created_at.asc()
            )
            .all()
        )

    # =========================================================
    # GET COMMENT BY ID
    # Giữ nguyên trả về Comments để service update/delete
    # không bị lỗi
    # =========================================================

    def get_by_id(self, comment_id):
        return (
            self.session.query(Comments)
            .filter(
                Comments.id == comment_id
            )
            .first()
        )

    # =========================================================
    # CREATE
    # =========================================================

    def create(self, comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

        return comment

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, comment):
        self.session.commit()
        self.session.refresh(comment)

        return comment

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self, comment):
        self.session.delete(comment)
        self.session.commit()

    # =========================================================
    # GET COMMENTS BY POST + USER INFO
    # =========================================================

    def list_for_post(self, post_id):
        return (
            self.session.query(Comments, Users)
            .outerjoin(
                Users,
                Comments.author_id == Users.id
            )
            .filter(
                Comments.post_id == post_id
            )
            .order_by(
                Comments.created_at.asc()
            )
            .all()
        )