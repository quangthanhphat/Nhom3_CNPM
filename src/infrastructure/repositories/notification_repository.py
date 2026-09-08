from infrastructure.models.generated_models import Notifications
from infrastructure.databases.factory_database import FactoryDatabase as db_factory


class NotificationRepository:
    def __init__(self):
        self.session = db_factory.get_database('POSTGREE').session

    def list_all(self):
        return self.session.query(Notifications).all()

    def get_by_id(self, notification_id):
        return (
            self.session.query(Notifications)
            .filter(Notifications.id == notification_id)
            .first()
        )

    def get_by_user_id(self, user_id):
        return (
            self.session.query(Notifications)
            .filter(Notifications.user_id == user_id)
            .all()
        )

    def create(self, notification):
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def update(self, notification):
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def delete(self, notification):
        self.session.delete(notification)
        self.session.commit()
        return True