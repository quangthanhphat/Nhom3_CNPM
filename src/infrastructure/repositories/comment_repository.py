from infrastructure.models.generated_models import Comments
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class CommentRepository:

    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Comments).all()

    def get_by_id(self, comment_id):
        return self.session.query(Comments).filter(
            Comments.id == comment_id
        ).first()

    def create(self, comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

        return comment

    def update(self, comment):
        self.session.commit()
        self.session.refresh(comment)

        return comment

    def delete(self, comment):
        self.session.delete(comment)
        self.session.commit()