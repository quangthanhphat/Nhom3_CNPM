from datetime import date

from infrastructure.models.digital_scan_model import DigitalScanModel
from infrastructure.repositories.digital_scan_repository import (
    DigitalScanRepository
)


class DigitalScanService:

    def __init__(self):
        self.repository = DigitalScanRepository()

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        scans = self.repository.list_all()

        # Admin được xem tất cả
        if role == 'admin':
            return scans

        # Customer chỉ xem scan của mình
        if role == 'customer':
            return [
                scan
                for scan in scans
                if str(scan.customer_id) == str(user_id)
            ]

        return []

    def get_by_id(self, scan_id):
        return self.repository.find_by_id(scan_id)

    def get_by_id_for_user(self, scan_id, user_id, role):
        scan = self.repository.find_by_id(scan_id)

        if not scan:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return scan, None

        # Customer chỉ xem scan của mình
        if role == 'customer':
            if str(scan.customer_id) != str(user_id):
                return None, 'forbidden'

            return scan, None

        return None, 'forbidden'

    def create(self, customer_id, data):
        shooting_date = data.get('shooting_date')

        if shooting_date:
            shooting_date = date.fromisoformat(shooting_date)

        scan = DigitalScanModel(
            order_id=data.get('order_id'),
            customer_id=customer_id,
            file_name=data.get('file_name'),
            storage_path=data.get('storage_path'),
            file_size=data.get('file_size'),
            scan_specification=data.get(
                'scan_specification'
            ),
            scan_quality=data.get('scan_quality'),
            film_stock=data.get('film_stock'),
            camera_model=data.get('camera_model'),
            lens=data.get('lens'),
            shooting_date=shooting_date,
            processing_method=data.get(
                'processing_method'
            )
        )

        return self.repository.create(scan)

    def update(
        self,
        scan_id,
        data,
        user_id,
        role
    ):
        scan, error = self.get_by_id_for_user(
            scan_id=scan_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        if 'file_name' in data:
            scan.file_name = data['file_name']

        if 'storage_path' in data:
            scan.storage_path = data['storage_path']

        if 'file_size' in data:
            scan.file_size = data['file_size']

        if 'scan_specification' in data:
            scan.scan_specification = data[
                'scan_specification'
            ]

        if 'scan_quality' in data:
            scan.scan_quality = data['scan_quality']

        if 'film_stock' in data:
            scan.film_stock = data['film_stock']

        if 'camera_model' in data:
            scan.camera_model = data['camera_model']

        if 'lens' in data:
            scan.lens = data['lens']

        if 'shooting_date' in data:
            shooting_date = data['shooting_date']

            if shooting_date:
                shooting_date = date.fromisoformat(
                    shooting_date
                )

            scan.shooting_date = shooting_date

        if 'processing_method' in data:
            scan.processing_method = data[
                'processing_method'
            ]

        return self.repository.update(scan), None

    def delete(
        self,
        scan_id,
        user_id,
        role
    ):
        scan, error = self.get_by_id_for_user(
            scan_id=scan_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        return self.repository.delete(scan), None