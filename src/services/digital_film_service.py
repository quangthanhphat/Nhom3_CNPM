import datetime

from infrastructure.models.generated_models import (
    ArchiveItems,
    DigitalFilmArchives,
    DigitalScans,
)
from infrastructure.repositories.digital_film_repository import DigitalFilmRepository


class DigitalFilmService:
    def __init__(self):
        self.repository = DigitalFilmRepository()

    def list_archives(self, customer_id):
        return self.repository.list_archives(customer_id)

    def get_archive(self, archive_id, customer_id):
        return self.repository.get_archive(archive_id, customer_id)

    def create_archive(self, customer_id, data):
        name = data.get('name')
        if not name:
            return None

        return self.repository.create_archive(DigitalFilmArchives(
            customer_id=customer_id,
            name=name,
            description=data.get('description')
        ))

    def update_archive(self, archive_id, customer_id, data):
        archive = self.repository.get_archive(archive_id, customer_id)
        if not archive:
            return None

        if 'name' in data:
            archive.name = data['name']
        if 'description' in data:
            archive.description = data['description']
        archive.updated_at = datetime.datetime.utcnow()
        return self.repository.update_archive(archive)

    def delete_archive(self, archive_id, customer_id):
        archive = self.repository.get_archive(archive_id, customer_id)
        if not archive:
            return False

        self.repository.delete_archive(archive)
        return True

    def list_scans(self, customer_id):
        return self.repository.list_scans(customer_id)

    def get_scan(self, scan_id, customer_id):
        return self.repository.get_scan(scan_id, customer_id)

    def create_scan(self, customer_id, data):
        required = ('order_id', 'file_name', 'storage_path')
        if any(not data.get(field) for field in required):
            return None

        return self.repository.create_scan(DigitalScans(
            order_id=data['order_id'],
            customer_id=customer_id,
            file_name=data['file_name'],
            storage_path=data['storage_path'],
            file_size=data.get('file_size'),
            scan_specification=data.get('scan_specification'),
            scan_quality=data.get('scan_quality'),
            film_stock=data.get('film_stock'),
            camera_model=data.get('camera_model'),
            lens=data.get('lens'),
            shooting_date=data.get('shooting_date'),
            processing_method=data.get('processing_method')
        ))

    def update_scan(self, scan_id, customer_id, data):
        scan = self.repository.get_scan(scan_id, customer_id)
        if not scan:
            return None

        editable_fields = (
            'file_name', 'storage_path', 'file_size', 'scan_specification',
            'scan_quality', 'film_stock', 'camera_model', 'lens',
            'shooting_date', 'processing_method'
        )
        for field in editable_fields:
            if field in data:
                setattr(scan, field, data[field])
        return self.repository.update_scan(scan)

    def delete_scan(self, scan_id, customer_id):
        scan = self.repository.get_scan(scan_id, customer_id)
        if not scan:
            return False

        self.repository.delete_scan(scan)
        return True

    def add_scan_to_archive(self, archive_id, scan_id, customer_id):
        archive = self.repository.get_archive(archive_id, customer_id)
        scan = self.repository.get_scan(scan_id, customer_id)
        if not archive or not scan:
            return None

        item = self.repository.get_archive_item(archive_id, scan_id)
        if item:
            return item

        return self.repository.add_scan_to_archive(ArchiveItems(
            archive_id=archive_id,
            scan_id=scan_id
        ))

    def remove_scan_from_archive(self, archive_id, scan_id, customer_id):
        if not self.repository.get_archive(archive_id, customer_id):
            return False
        item = self.repository.get_archive_item(archive_id, scan_id)
        if not item:
            return False

        self.repository.remove_scan_from_archive(item)
        return True
