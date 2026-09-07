from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.generated_models import Comments, Posts


class CommunityRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def list_posts(self, status=None):
        query = self.session.query(Posts).order_by(Posts.created_at.desc())
        if status:
            query = query.filter(Posts.status == status)
        return query.all()

    def get_post(self, post_id):
        return self.session.query(Posts).filter(Posts.id == post_id).first()

    def create_post(self, post):
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def save_post(self, post):
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete_post(self, post):
        self.session.delete(post)
        self.session.commit()

    def list_comments(self, post_id):
        return (self.session.query(Comments)
                .filter(Comments.post_id == post_id)
                .order_by(Comments.created_at.asc()).all())

    def get_comment(self, comment_id):
        return self.session.query(Comments).filter(Comments.id == comment_id).first()

    def create_comment(self, comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def save_comment(self, comment):
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def delete_comment(self, comment):
        self.session.delete(comment)
        self.session.commit()
