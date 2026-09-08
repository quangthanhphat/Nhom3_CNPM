from infrastructure.models.generated_models import Notifications


class NotificationService:
    def __init__(self, repository):
        self.repository = repository

    def list_for_user(self, user_id, is_admin=False):
        if is_admin:
            return self.repository.list_all()

        return self.repository.get_by_user_id(user_id)

    def get_by_id_for_user(self, notification_id, user_id, is_admin=False):
        notification = self.repository.get_by_id(notification_id)

        if not notification:
            return None, "Notification not found"

        if not is_admin and notification.user_id != user_id:
            return None, "Forbidden"

        return notification, None

    def create(self, data):
        notification = Notifications(
            user_id=data.get("user_id"),
            title=data.get("title"),
            message=data.get("message"),
            is_read=data.get("is_read", False)
        )

        return self.repository.create(notification), None

    def mark_as_read(self, notification_id, user_id, is_admin=False):
        notification, error = self.get_by_id_for_user(
            notification_id,
            user_id,
            is_admin
        )

        if error:
            return None, error

        notification.is_read = True

        return self.repository.update(notification), None

    def delete(self, notification_id, user_id, is_admin=False):
        notification, error = self.get_by_id_for_user(
            notification_id,
            user_id,
            is_admin
        )

        if error:
            return False, error

        self.repository.delete(notification)

        return True, None