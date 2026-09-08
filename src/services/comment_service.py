
from infrastructure.repositories.comment_repository import CommentRepository
from infrastructure.models.generated_models import Comments

class CommentService:

    def __init__(self):
        self.repository = CommentRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        comments = self.repository.list_all()

        # Tất cả role đều được xem comment
        return comments

    def get_by_id(self, comment_id):
        return self.repository.get_by_id(comment_id)

    def get_by_id_for_user(self, comment_id, user_id, role):
        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None, 'not_found'

        # Tất cả role đều được xem comment
        return comment, None

    def create(self, author_id, data):
        comment = Comments(
            author_id=author_id,
            post_id=data.get('post_id'),
            content=data.get('content')
        )

        return self.repository.create(comment)

    def update(self, comment_id, data, user_id, role):
        comment, error = self.get_by_id_for_user(
            comment_id=comment_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Admin được sửa tất cả
        if role != 'admin':
            if str(comment.author_id) != str(user_id):
                return None, 'forbidden'

        if 'content' in data:
            comment.content = data.get('content')

        return self.repository.update(comment), None

    def delete(self, comment_id, user_id, role):
        comment, error = self.get_by_id_for_user(
            comment_id=comment_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        # Admin được xóa tất cả
        if role != 'admin':
            if str(comment.author_id) != str(user_id):
                return False, 'forbidden'

        self.repository.delete(comment)

        return True, None