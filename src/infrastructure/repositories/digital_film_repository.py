from infrastructure.models.generated_models import (
    ArchiveItems,
    DigitalFilmArchives,
    DigitalScans,
)
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class DigitalFilmRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_archives(self, customer_id):
        return self.session.query(DigitalFilmArchives).filter(
            DigitalFilmArchives.customer_id == customer_id
        ).order_by(DigitalFilmArchives.created_at.desc()).all()

    def get_archive(self, archive_id, customer_id):
        return self.session.query(DigitalFilmArchives).filter(
            DigitalFilmArchives.id == archive_id,
            DigitalFilmArchives.customer_id == customer_id
        ).first()

    def create_archive(self, archive):
        self.session.add(archive)
        self.session.commit()
        self.session.refresh(archive)
        return archive

    def update_archive(self, archive):
        self.session.commit()
        self.session.refresh(archive)
        return archive

    def delete_archive(self, archive):
        self.session.delete(archive)
        self.session.commit()

    def get_scan(self, scan_id, customer_id):
        return self.session.query(DigitalScans).filter(
            DigitalScans.id == scan_id,
            DigitalScans.customer_id == customer_id
        ).first()

    def list_scans(self, customer_id):
        return self.session.query(DigitalScans).filter(
            DigitalScans.customer_id == customer_id
        ).order_by(DigitalScans.uploaded_at.desc()).all()

    def create_scan(self, scan):
        self.session.add(scan)
        self.session.commit()
        self.session.refresh(scan)
        return scan

    def update_scan(self, scan):
        self.session.commit()
        self.session.refresh(scan)
        return scan

    def delete_scan(self, scan):
        self.session.delete(scan)
        self.session.commit()

    def get_archive_item(self, archive_id, scan_id):
        return self.session.query(ArchiveItems).filter(
            ArchiveItems.archive_id == archive_id,
            ArchiveItems.scan_id == scan_id
        ).first()

    def add_scan_to_archive(self, item):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def remove_scan_from_archive(self, item):
        self.session.delete(item)
        self.session.commit()
