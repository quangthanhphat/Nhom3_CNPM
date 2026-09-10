from infrastructure.models.support_model import SupportModel
from infrastructure.repositories.support_repository import SupportRepository


class SupportService:

    def __init__(self, repository):
        self.repository = repository

    # =========================================================
    # LIST
    # =========================================================

    def list_all(self):
        return self.repository.list_all()

    def list_for_user(self, user_id, role):
        # Admin xem toàn bộ yêu cầu Support
        if role == 'admin':
            return self.repository.list_all()

        # Owner chỉ xem các yêu cầu do chính mình gửi
        if role == 'film_lab_owner':
            return self.repository.list_by_user(user_id)

        return []

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(self, support_id):
        return self.repository.find_by_id(support_id)

    def get_by_id_for_user(
        self,
        support_id,
        user_id,
        role
    ):
        support = self.repository.find_by_id(
            support_id
        )

        if not support:
            return None, 'not_found'

        # Admin được xem tất cả
        if role == 'admin':
            return support, None

        # Owner chỉ được xem ticket của chính mình
        if role == 'film_lab_owner':
            if str(support.user_id) != str(user_id):
                return None, 'forbidden'

            return support, None

        return None, 'forbidden'

    # =========================================================
    # CREATE SUPPORT TICKET
    # =========================================================

    def create(
        self,
        user_id,
        data
    ):
        subject = data.get('subject')
        message = data.get('message')

        if not subject:
            return None, 'subject_required'

        if not message:
            return None, 'message_required'

        support = SupportModel(
            user_id=user_id,
            subject=subject,
            message=message,
            reply=None,
            status='open'
        )

        support = self.repository.create(
            support
        )

        return support, None

    # =========================================================
    # REPLY
    # =========================================================

    def reply(
        self,
        support_id,
        reply,
        user_id,
        role
    ):
        support, error = self.get_by_id_for_user(
            support_id=support_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Chỉ Admin được trả lời
        if role != 'admin':
            return None, 'forbidden'

        if not reply:
            return None, 'reply_required'

        support.reply = reply
        support.status = 'answered'

        return self.repository.update(
            support
        ), None

    # =========================================================
    # CLOSE
    # =========================================================

    def close(
        self,
        support_id,
        user_id,
        role
    ):
        support, error = self.get_by_id_for_user(
            support_id=support_id,
            user_id=user_id,
            role=role
        )

        if error:
            return None, error

        # Chỉ Admin được đóng ticket
        if role != 'admin':
            return None, 'forbidden'

        support.status = 'closed'

        return self.repository.update(
            support
        ), None

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        support_id,
        user_id,
        role
    ):
        support, error = self.get_by_id_for_user(
            support_id=support_id,
            user_id=user_id,
            role=role
        )

        if error:
            return False, error

        # Chỉ Admin được xóa
        if role != 'admin':
            return False, 'forbidden'

        self.repository.delete(
            support
        )

        return True, None