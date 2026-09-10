from infrastructure.databases import FactoryDatabase
from infrastructure.models.archive_item_model import ArchiveItemModel
from infrastructure.models.digital_scan_model import DigitalScanModel


class ArchiveItemRepository:

    def __init__(self):
        self.database = FactoryDatabase.get_database('POSTGREE')

    def list_all(self):
        session = self.database.session

        return session.query(ArchiveItemModel).all()

    def find_by_id(self, archive_item_id):
        session = self.database.session

        return session.query(ArchiveItemModel).filter(
            ArchiveItemModel.id == archive_item_id
        ).first()

    def list_by_archive_id(self, archive_id):
        session = self.database.session

        return (
            session.query(ArchiveItemModel, DigitalScanModel)
            .join(
                DigitalScanModel,
                ArchiveItemModel.scan_id == DigitalScanModel.id
            )
            .filter(
                ArchiveItemModel.archive_id == archive_id
            )
            .order_by(
                ArchiveItemModel.added_at.asc()
            )
            .all()
        )

    def find_by_archive_and_scan(self, archive_id, scan_id):
        session = self.database.session

        return (
            session.query(ArchiveItemModel)
            .filter(
                ArchiveItemModel.archive_id == archive_id,
                ArchiveItemModel.scan_id == scan_id
            )
            .first()
        )

    def create(self, archive_item):
        session = self.database.session

        try:
            session.add(archive_item)
            session.commit()
            session.refresh(archive_item)

            return archive_item

        except Exception:
            session.rollback()
            raise

    def update(self, archive_item):
        session = self.database.session

        try:
            session.commit()
            session.refresh(archive_item)

            return archive_item

        except Exception:
            session.rollback()
            raise

    def delete(self, archive_item):
        session = self.database.session

        try:
            session.delete(archive_item)
            session.commit()

            return True

        except Exception:
            session.rollback()
            raise