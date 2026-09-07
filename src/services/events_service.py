from datetime import datetime, timezone
from uuid import UUID

from infrastructure.models.generated_models import (
    PhotowalkRegistrations,
    Photowalks,
    WorkshopRegistrations,
    Workshops,
)
from infrastructure.repositories.events_repository import EventsRepository


class EventsService:
    def __init__(self, repository=None):
        self.repository = repository or EventsRepository()

    @staticmethod
    def _uuid(value, field):
        try:
            return UUID(str(value))
        except (TypeError, ValueError):
            raise ValueError(f'{field} must be a valid UUID')

    @staticmethod
    def _date(value, field):
        if not value:
            raise ValueError(f'{field} is required')
        try:
            parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return parsed.astimezone(timezone.utc).replace(tzinfo=None) if parsed.tzinfo else parsed
        except (TypeError, ValueError):
            raise ValueError(f'{field} must be an ISO 8601 datetime')

    @staticmethod
    def _required(data, fields):
        missing = [field for field in fields if not data.get(field)]
        if missing:
            raise ValueError(f'Missing required fields: {", ".join(missing)}')

    def _event_data(self, data):
        self._required(data, ('title', 'start_time'))
        start_time = self._date(data['start_time'], 'start_time')
        end_time = self._date(data['end_time'], 'end_time') if data.get('end_time') else None
        if end_time and end_time <= start_time:
            raise ValueError('end_time must be after start_time')
        return start_time, end_time

    def list_workshops(self, status=None): return self.repository.list_workshops(status)
    def get_workshop(self, event_id): return self.repository.get_workshop(self._uuid(event_id, 'workshop_id'))

    def create_workshop(self, user_id, data):
        start, end = self._event_data(data)
        return self.repository.create_workshop(Workshops(
            organizer_id=self._uuid(user_id, 'user_id'), title=data['title'],
            start_time=start, end_time=end, description=data.get('description'),
            location=data.get('location'), status=data.get('status', 'upcoming')))

    def update_workshop(self, event_id, user_id, data):
        event = self.get_workshop(event_id)
        if not event: return None
        if event.organizer_id != self._uuid(user_id, 'user_id'):
            raise PermissionError('Only the organizer can update this workshop')
        values = dict(data)
        if 'start_time' in values or 'end_time' in values:
            values['start_time'] = values.get('start_time', event.start_time.isoformat())
            start, end = self._event_data(values)
            event.start_time, event.end_time = start, end
        for field in ('title', 'description', 'location', 'status'):
            if field in data:
                if field == 'title' and not data[field]: raise ValueError('title cannot be empty')
                setattr(event, field, data[field])
        return self.repository.save_workshop(event)

    def delete_workshop(self, event_id, user_id):
        event = self.get_workshop(event_id)
        if not event: return False
        if event.organizer_id != self._uuid(user_id, 'user_id'): raise PermissionError('Only the organizer can delete this workshop')
        self.repository.delete_workshop(event); return True

    def register_workshop(self, event_id, user_id):
        event = self.get_workshop(event_id)
        if not event: return None
        user = self._uuid(user_id, 'user_id')
        registration = self.repository.get_workshop_registration(event.id, user)
        if registration: raise RuntimeError('User is already registered for this workshop')
        return self.repository.create_workshop_registration(WorkshopRegistrations(workshop_id=event.id, user_id=user))

    def list_workshop_registrations(self, event_id):
        event = self.get_workshop(event_id)
        return None if not event else self.repository.list_workshop_registrations(event.id)

    def cancel_workshop(self, event_id, user_id):
        registration = self.repository.get_workshop_registration(self._uuid(event_id, 'workshop_id'), self._uuid(user_id, 'user_id'))
        if not registration: return False
        registration.status = 'cancelled'; registration.cancelled_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.repository.save_workshop_registration(registration); return True

    def list_photowalks(self, status=None): return self.repository.list_photowalks(status)
    def get_photowalk(self, event_id): return self.repository.get_photowalk(self._uuid(event_id, 'photowalk_id'))

    def create_photowalk(self, user_id, data):
        start, end = self._event_data(data)
        return self.repository.create_photowalk(Photowalks(
            organizer_id=self._uuid(user_id, 'user_id'), title=data['title'],
            start_time=start, end_time=end, description=data.get('description'),
            meeting_location=data.get('meeting_location'), status=data.get('status', 'upcoming')))

    def update_photowalk(self, event_id, user_id, data):
        event = self.get_photowalk(event_id)
        if not event: return None
        if event.organizer_id != self._uuid(user_id, 'user_id'): raise PermissionError('Only the organizer can update this photowalk')
        values = dict(data)
        if 'start_time' in values or 'end_time' in values:
            values['start_time'] = values.get('start_time', event.start_time.isoformat())
            start, end = self._event_data(values); event.start_time, event.end_time = start, end
        for field in ('title', 'description', 'meeting_location', 'status'):
            if field in data:
                if field == 'title' and not data[field]: raise ValueError('title cannot be empty')
                setattr(event, field, data[field])
        return self.repository.save_photowalk(event)

    def delete_photowalk(self, event_id, user_id):
        event = self.get_photowalk(event_id)
        if not event: return False
        if event.organizer_id != self._uuid(user_id, 'user_id'): raise PermissionError('Only the organizer can delete this photowalk')
        self.repository.delete_photowalk(event); return True

    def register_photowalk(self, event_id, user_id):
        event = self.get_photowalk(event_id)
        if not event: return None
        user = self._uuid(user_id, 'user_id')
        registration = self.repository.get_photowalk_registration(event.id, user)
        if registration: raise RuntimeError('User is already registered for this photowalk')
        return self.repository.create_photowalk_registration(PhotowalkRegistrations(photowalk_id=event.id, user_id=user))

    def list_photowalk_registrations(self, event_id):
        event = self.get_photowalk(event_id)
        return None if not event else self.repository.list_photowalk_registrations(event.id)

    def cancel_photowalk(self, event_id, user_id):
        registration = self.repository.get_photowalk_registration(self._uuid(event_id, 'photowalk_id'), self._uuid(user_id, 'user_id'))
        if not registration: return False
        registration.status = 'cancelled'; registration.cancelled_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.repository.save_photowalk_registration(registration); return True
