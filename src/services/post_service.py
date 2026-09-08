from infrastructure.models.post_model import PostModel
from infrastructure.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.repository = PostRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        posts = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return posts

        # Customer và Photography Expert chỉ xem được bài của mình
        if role in ['customer', 'photography_expert']:
            return [
                post
                for post in posts
                if str(post.author_id) == str(user_id)
            ]

        return []

    def get_by_id(self, post_id):
        return self.repository.get_by_id(post_id)

    def get_by_id_for_user(self, post_id, user_id, role):
        post = self.repository.get_by_id(post_id)

        if not post:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return post, None

        # Customer / Photography Expert chỉ xem bài của mình
        if role in ['customer', 'photography_expert']:
            if str(post.author_id) != str(user_id):
                return None, 'forbidden'

            return post, None

        return None, 'forbidden'

    def create(self, author_id, data):
        post = PostModel(
            author_id=author_id,
            type=data.get('type'),
            title=data.get('title'),
            content=data.get('content'),
            status=data.get('status', 'published')
        )

        return self.repository.create(post)

    def update(self, post_id, data, user_id, role):
        post, error = self.get_by_id_for_user(
            post_id=post_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        if 'type' in data:
            post.type = data.get('type')

        if 'title' in data:
            post.title = data.get('title')

        if 'content' in data:
            post.content = data.get('content')

        if 'status' in data:
            post.status = data.get('status')

        return self.repository.update(post), None

    def delete(self, post_id, user_id, role):
        post, error = self.get_by_id_for_user(
            post_id=post_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(post)

        return True, None