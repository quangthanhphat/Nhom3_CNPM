from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.generated_models import (
    PhotowalkRegistrations,
    Photowalks,
    WorkshopRegistrations,
    Workshops,
)


class EventsRepository:
    def __init__(self, session=None):
        self.session = session or db_factory.get_database('POSTGREE').session

    def list_workshops(self, status=None):
        query = self.session.query(Workshops).order_by(Workshops.start_time.asc())
        if status:
            query = query.filter(Workshops.status == status)
        return query.all()

    def get_workshop(self, event_id):
        return self.session.query(Workshops).filter(Workshops.id == event_id).first()

    def create_workshop(self, event):
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def save_workshop(self, event):
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete_workshop(self, event):
        self.session.delete(event)
        self.session.commit()

    def list_photowalks(self, status=None):
        query = self.session.query(Photowalks).order_by(Photowalks.start_time.asc())
        if status:
            query = query.filter(Photowalks.status == status)
        return query.all()

    def get_photowalk(self, event_id):
        return self.session.query(Photowalks).filter(Photowalks.id == event_id).first()

    def create_photowalk(self, event):
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def save_photowalk(self, event):
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete_photowalk(self, event):
        self.session.delete(event)
        self.session.commit()

    def get_workshop_registration(self, event_id, user_id):
        return (self.session.query(WorkshopRegistrations)
                .filter(WorkshopRegistrations.workshop_id == event_id,
                        WorkshopRegistrations.user_id == user_id,
                        WorkshopRegistrations.status == 'registered').first())

    def list_workshop_registrations(self, event_id):
        return (self.session.query(WorkshopRegistrations)
                .filter(WorkshopRegistrations.workshop_id == event_id).all())

    def create_workshop_registration(self, registration):
        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)
        return registration

    def save_workshop_registration(self, registration):
        self.session.commit()
        self.session.refresh(registration)
        return registration

    def get_photowalk_registration(self, event_id, user_id):
        return (self.session.query(PhotowalkRegistrations)
                .filter(PhotowalkRegistrations.photowalk_id == event_id,
                        PhotowalkRegistrations.user_id == user_id,
                        PhotowalkRegistrations.status == 'registered').first())

    def list_photowalk_registrations(self, event_id):
        return (self.session.query(PhotowalkRegistrations)
                .filter(PhotowalkRegistrations.photowalk_id == event_id).all())

    def create_photowalk_registration(self, registration):
        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)
        return registration

    def save_photowalk_registration(self, registration):
        self.session.commit()
        self.session.refresh(registration)
        return registration
