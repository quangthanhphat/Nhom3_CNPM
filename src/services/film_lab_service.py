from infrastructure.models.generated_models import FilmLabs
from infrastructure.repositories.film_lab_repository import FilmLabRepository
from services.storage_service import StorageService


class FilmLabService:
    def __init__(self):
        self.repository = FilmLabRepository()

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, film_lab_id):
        return self.repository.get_by_id(film_lab_id)

    def create(self, owner_id, data):
        film_lab = FilmLabs(
            owner_id=owner_id,
            name=data.get('name'),
            description=data.get('description'),
            city=data.get('city'),
            district=data.get('district'),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get('email')
        )

        return self.repository.create(film_lab)

    def update(
        self,
        film_lab_id,
        data,
        user_id=None,
        is_admin=False
    ):
        film_lab = self.repository.get_by_id(film_lab_id)

        if not film_lab:
            return None, 'not_found'

        # Admin được quản lý tất cả Film Lab.
        # Film Lab Owner chỉ được sửa Film Lab của chính mình.
        if (
            not is_admin
            and str(film_lab.owner_id) != str(user_id)
        ):
            return None, 'forbidden'

        film_lab.name = data.get(
            'name',
            film_lab.name
        )

        film_lab.description = data.get(
            'description',
            film_lab.description
        )

        film_lab.city = data.get(
            'city',
            film_lab.city
        )

        film_lab.district = data.get(
            'district',
            film_lab.district
        )

        film_lab.address = data.get(
            'address',
            film_lab.address
        )

        film_lab.phone = data.get(
            'phone',
            film_lab.phone
        )

        film_lab.email = data.get(
            'email',
            film_lab.email
        )

        return self.repository.update(
            film_lab
        ), None

    def update_profile_image(
        self,
        film_lab_id,
        image_file,
        user_id=None,
        is_admin=False
    ):
        film_lab = self.repository.get_by_id(
            film_lab_id
        )

        if not film_lab:
            return None, 'not_found'

        if (
            not is_admin
            and str(film_lab.owner_id) != str(user_id)
        ):
            return None, 'forbidden'

        new_path = StorageService.replace_file(
            file=image_file,
            old_storage_path=film_lab.profile_image_path,
            folder='film_labs/profile'
        )

        film_lab.profile_image_path = new_path

        self.repository.update(film_lab)

        return film_lab, None

    def update_cover_image(
        self,
        film_lab_id,
        image_file,
        user_id=None,
        is_admin=False
    ):
        film_lab = self.repository.get_by_id(
            film_lab_id
        )

        if not film_lab:
            return None, 'not_found'

        if (
            not is_admin
            and str(film_lab.owner_id) != str(user_id)
        ):
            return None, 'forbidden'

        new_path = StorageService.replace_file(
            file=image_file,
            old_storage_path=film_lab.cover_image_path,
            folder='film_labs/cover'
        )

        film_lab.cover_image_path = new_path

        self.repository.update(film_lab)

        return film_lab, None

    def delete(self, film_lab_id, user_id=None, is_admin=False):
        film_lab = self.repository.get_by_id(
            film_lab_id
        )

        if not film_lab:
            return False, 'not_found'

        # Admin được xóa tất cả.
        # Film Lab Owner chỉ được xóa Film Lab của chính mình.
        if (
            not is_admin
            and str(film_lab.owner_id) != str(user_id)
        ):
            return False, 'forbidden'

        self.repository.delete(film_lab)

        return True, None