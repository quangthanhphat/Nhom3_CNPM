from datetime import datetime, timezone
from uuid import UUID

from infrastructure.models.generated_models import Comments, Posts
from infrastructure.repositories.community_repository import CommunityRepository


class CommunityService:
    def __init__(self, repository=None):
        self.repository = repository or CommunityRepository()

    @staticmethod
    def _uuid(value, field):
        try:
            return UUID(str(value))
        except (TypeError, ValueError):
            raise ValueError(f'{field} must be a valid UUID')

    @staticmethod
    def _required(data, fields):
        missing = [field for field in fields if not data.get(field)]
        if missing:
            raise ValueError(f'Missing required fields: {", ".join(missing)}')

    def list_posts(self, status=None):
        return self.repository.list_posts(status)

    def get_post(self, post_id):
        return self.repository.get_post(self._uuid(post_id, 'post_id'))

    def create_post(self, user_id, data):
        self._required(data, ('type', 'title', 'content'))
        post = Posts(author_id=self._uuid(user_id, 'user_id'), type=data['type'],
                     title=data['title'], content=data['content'],
                     status=data.get('status', 'published'))
        return self.repository.create_post(post)

    def update_post(self, post_id, user_id, data):
        post = self.get_post(post_id)
        if not post:
            return None
        if post.author_id != self._uuid(user_id, 'user_id'):
            raise PermissionError('Only the author can update this post')
        for field in ('type', 'title', 'content', 'status'):
            if field in data:
                if not data[field]:
                    raise ValueError(f'{field} cannot be empty')
                setattr(post, field, data[field])
        post.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return self.repository.save_post(post)

    def delete_post(self, post_id, user_id):
        post = self.get_post(post_id)
        if not post:
            return False
        if post.author_id != self._uuid(user_id, 'user_id'):
            raise PermissionError('Only the author can delete this post')
        self.repository.delete_post(post)
        return True

    def list_comments(self, post_id):
        post = self.get_post(post_id)
        if not post:
            return None
        return self.repository.list_comments(post.id)

    def create_comment(self, post_id, user_id, data):
        self._required(data, ('content',))
        post = self.get_post(post_id)
        if not post:
            return None
        comment = Comments(post_id=post.id, author_id=self._uuid(user_id, 'user_id'),
                           content=data['content'])
        return self.repository.create_comment(comment)

    def update_comment(self, comment_id, user_id, data):
        comment = self.repository.get_comment(self._uuid(comment_id, 'comment_id'))
        if not comment:
            return None
        if comment.author_id != self._uuid(user_id, 'user_id'):
            raise PermissionError('Only the author can update this comment')
        if not data.get('content'):
            raise ValueError('content cannot be empty')
        comment.content = data['content']
        comment.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return self.repository.save_comment(comment)

    def delete_comment(self, comment_id, user_id):
        comment = self.repository.get_comment(self._uuid(comment_id, 'comment_id'))
        if not comment:
            return False
        if comment.author_id != self._uuid(user_id, 'user_id'):
            raise PermissionError('Only the author can delete this comment')
        self.repository.delete_comment(comment)
        return True
