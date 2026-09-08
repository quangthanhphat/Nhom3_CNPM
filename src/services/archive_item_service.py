from infrastructure.models.archive_item_model import ArchiveItemModel
from infrastructure.repositories.archive_item_repository import (
    ArchiveItemRepository
)
from infrastructure.repositories.digital_film_archive_repository import (
    DigitalFilmArchiveRepository
)
from infrastructure.repositories.digital_scan_repository import (
    DigitalScanRepository
)


class ArchiveItemService:

    def __init__(self):
        self.repository = ArchiveItemRepository()
        self.archive_repository = DigitalFilmArchiveRepository()
        self.scan_repository = DigitalScanRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        items = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return items

        if role != 'customer':
            return []

        result = []

        for item in items:
            archive = self.archive_repository.get_by_id(
                item.archive_id
            )

            if (
                archive
                and str(archive.customer_id) == str(user_id)
            ):
                result.append(item)

        return result

    def get_by_id(self, archive_item_id):
        return self.repository.find_by_id(archive_item_id)

    def get_by_id_for_user(
        self,
        archive_item_id,
        user_id,
        role
    ):
        item = self.repository.find_by_id(
            archive_item_id
        )

        if not item:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return item, None

        if role != 'customer':
            return None, 'forbidden'

        archive = self.archive_repository.get_by_id(
            item.archive_id
        )

        if not archive:
            return None, 'not_found'

        if str(archive.customer_id) != str(user_id):
            return None, 'forbidden'

        return item, None

    def create(self, data, user_id, role):
        archive_id = data.get('archive_id')
        scan_id = data.get('scan_id')

        archive = self.archive_repository.get_by_id(
            archive_id
        )

        if not archive:
            return None, 'archive_not_found'

        scan = self.scan_repository.find_by_id(
            scan_id
        )

        if not scan:
            return None, 'scan_not_found'

        # Admin được thêm scan vào bất kỳ archive nào
        if role == 'admin':
            pass

        elif role == 'customer':
            # Archive phải thuộc customer hiện tại
            if str(archive.customer_id) != str(user_id):
                return None, 'forbidden'

            # Scan cũng phải thuộc customer hiện tại
            if str(scan.customer_id) != str(user_id):
                return None, 'forbidden'

        else:
            return None, 'forbidden'

        archive_item = ArchiveItemModel(
            archive_id=archive_id,
            scan_id=scan_id
        )

        return self.repository.create(archive_item), None

    def update(
        self,
        archive_item_id,
        data,
        user_id,
        role
    ):
        item, error = self.get_by_id_for_user(
            archive_item_id=archive_item_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        new_archive_id = data.get('archive_id')
        new_scan_id = data.get('scan_id')

        # Nếu đổi Archive thì phải kiểm tra ownership
        if new_archive_id:
            archive = self.archive_repository.get_by_id(
                new_archive_id
            )

            if not archive:
                return None, 'archive_not_found'

            if role == 'customer':
                if str(archive.customer_id) != str(user_id):
                    return None, 'forbidden'

            item.archive_id = new_archive_id

        # Nếu đổi Scan thì phải kiểm tra ownership
        if new_scan_id:
            scan = self.scan_repository.find_by_id(
                new_scan_id
            )

            if not scan:
                return None, 'scan_not_found'

            if role == 'customer':
                if str(scan.customer_id) != str(user_id):
                    return None, 'forbidden'

            item.scan_id = new_scan_id

        return self.repository.update(item), None

    def delete(
        self,
        archive_item_id,
        user_id,
        role
    ):
        item, error = self.get_by_id_for_user(
            archive_item_id=archive_item_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        self.repository.delete(item)

        return True, None