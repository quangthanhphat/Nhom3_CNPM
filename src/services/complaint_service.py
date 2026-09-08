from infrastructure.models.generated_models import Complaints


class ComplaintService:
    def __init__(self, repository):
        self.repository = repository

    def list_for_user(self, user_id, is_admin=False):
        if is_admin:
            return self.repository.get_all()

        return self.repository.get_by_user_id(user_id)

    def get_by_id_for_user(self, complaint_id, user_id, is_admin=False):
        complaint = self.repository.get_by_id(complaint_id)

        if not complaint:
            return None, "Complaint not found"

        if not is_admin and complaint.user_id != user_id:
            return None, "Access denied"

        return complaint, None

    def create(self, user_id, data):
        complaint = Complaints(
            user_id=user_id,
            type=data.get("type"),
            description=data.get("description"),
            status="pending"
        )

        return self.repository.create(complaint), None

    def update(self, complaint_id, user_id, data, is_admin=False):
        complaint, error = self.get_by_id_for_user(
            complaint_id,
            user_id,
            is_admin
        )

        if error:
            return None, error

        if "type" in data:
            complaint.type = data["type"]

        if "description" in data:
            complaint.description = data["description"]

        # Chỉ Admin xử lý trạng thái/kết quả complaint
        if is_admin:
            if "status" in data:
                complaint.status = data["status"]

            if "resolution" in data:
                complaint.resolution = data["resolution"]

            if "resolved_at" in data:
                complaint.resolved_at = data["resolved_at"]

        return self.repository.update(complaint), None

    def delete(self, complaint_id, user_id, is_admin=False):
        complaint, error = self.get_by_id_for_user(
            complaint_id,
            user_id,
            is_admin
        )

        if error:
            return False, error

        self.repository.delete(complaint)
        return True, None