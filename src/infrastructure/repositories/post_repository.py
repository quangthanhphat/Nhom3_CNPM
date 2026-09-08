from infrastructure.models.post_model import PostModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class PostRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(PostModel).all()

    def get_by_id(self, post_id):
        return self.session.query(PostModel).filter(
            PostModel.id == post_id
        ).first()

    def create(self, post):
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def update(self, post):
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post):
        self.session.delete(post)
        self.session.commit()
        