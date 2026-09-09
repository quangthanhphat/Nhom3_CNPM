from infrastructure.models.post_model import PostModel
from infrastructure.models.generated_models import PostImages
from infrastructure.repositories.post_repository import PostRepository
from services.storage_service import StorageService


class PostService:
    def __init__(self):
        self.repository = PostRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        posts = self.repository.list_all()

        # Community dùng chung:
        # Customer, Owner, Expert và Admin
        # đều được xem toàn bộ bài viết.
        return posts

    def get_by_id(self, post_id):
        return self.repository.get_by_id(post_id)

    def get_by_id_for_user(
        self,
        post_id,
        user_id,
        role
    ):
        post = self.repository.get_by_id(post_id)

        if not post:
            return None, 'not_found'

        # Community dùng chung:
        # tất cả role được xem bài viết.
        return post, None

    # =========================================================
    # CREATE POST
    # =========================================================

    def create(
        self,
        author_id,
        data,
        image_files=None
    ):
        post = PostModel(
            author_id=author_id,
            type=data.get('type'),
            title=data.get('title'),
            content=data.get('content'),
            status=data.get(
                'status',
                'published'
            )
        )

        # Lưu Post trước để PostgreSQL sinh post.id
        post = self.repository.create(post)

        # =====================================================
        # LƯU ẢNH
        # =====================================================

        if image_files:
            for image_file in image_files:
                image_path = StorageService.save_file(
                    file=image_file,
                    folder='posts'
                )

                post_image = PostImages(
                    post_id=post.id,
                    image_path=image_path
                )

                # Không dùng post.post_images
                # vì PostModel không có relationship này.
                self.repository.session.add(
                    post_image
                )

            self.repository.session.commit()

        # Refresh Post sau khi lưu ảnh
        self.repository.session.refresh(post)

        return post

    # =========================================================
    # UPDATE POST
    # =========================================================

    def update(
        self,
        post_id,
        data,
        user_id,
        role,
        image_files=None
    ):
        post, error = self.get_by_id_for_user(
            post_id=post_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Chỉ Admin hoặc chính tác giả được sửa bài
        if role != 'admin':
            if str(post.author_id) != str(user_id):
                return None, 'forbidden'

        if 'type' in data:
            post.type = data.get('type')

        if 'title' in data:
            post.title = data.get('title')

        if 'content' in data:
            post.content = data.get('content')

        if 'status' in data:
            post.status = data.get('status')

        # =====================================================
        # THÊM ẢNH MỚI
        # =====================================================

        if image_files:
            for image_file in image_files:
                image_path = StorageService.save_file(
                    file=image_file,
                    folder='posts'
                )

                post_image = PostImages(
                    post_id=post.id,
                    image_path=image_path
                )

                self.repository.session.add(
                    post_image
                )

        return self.repository.update(post), None

    # =========================================================
    # DELETE POST
    # =========================================================

    def delete(
        self,
        post_id,
        user_id,
        role
    ):
        post, error = self.get_by_id_for_user(
            post_id=post_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        # Chỉ Admin hoặc chính tác giả được xóa bài
        if role != 'admin':
            if str(post.author_id) != str(user_id):
                return False, 'forbidden'

        # =====================================================
        # LẤY CÁC ẢNH CỦA POST
        # =====================================================

        post_images = (
            self.repository.session
            .query(PostImages)
            .filter(
                PostImages.post_id == post.id
            )
            .all()
        )

        # Xóa file ảnh khỏi storage
        for post_image in post_images:
            StorageService.delete_file(
                post_image.image_path
            )

        # Xóa record PostImages
        for post_image in post_images:
            self.repository.session.delete(
                post_image
            )

        self.repository.session.commit()

        # Xóa Post
        self.repository.delete(post)

        return True, None