from infrastructure.databases import FactoryDatabase
from infrastructure.models.digital_scan_model import DigitalScanModel


class DigitalScanRepository:

    def __init__(self):
        self.database = FactoryDatabase.get_database('POSTGREE')

    def create(self, scan):
        session = self.database.session

        session.add(scan)
        session.commit()
        session.refresh(scan)

        return scan

    def list_all(self):
        session = self.database.session

        return session.query(DigitalScanModel).all()

    def find_by_id(self, scan_id):
        session = self.database.session

        return session.query(DigitalScanModel).filter(
            DigitalScanModel.id == scan_id
        ).first()

    def update(self, scan):
        session = self.database.session

        session.commit()
        session.refresh(scan)

        return scan

    def delete(self, scan):
        session = self.database.session

        session.delete(scan)
        session.commit()

        return True