from flask import Blueprint, request, jsonify

from api.middleware import token_required, role_required
from infrastructure.models.generated_models import Complaints

from infrastructure.repositories.complaint_repository import (
    ComplaintRepository
)
from services.complaint_service import ComplaintService


bp = Blueprint(
    "complaint",
    __name__,
    url_prefix="/api/complaints"
)


def complaint_to_dict(complaint):
    return {
        "id": str(complaint.id),
        "user_id": str(complaint.user_id),
        "type": complaint.type,
        "description": complaint.description,
        "status": complaint.status,
        "created_at": (
            complaint.created_at.isoformat()
            if complaint.created_at
            else None
        ),
        "resolution": complaint.resolution,
        "resolved_at": (
            complaint.resolved_at.isoformat()
            if complaint.resolved_at
            else None
        )
    }


@bp.route("", methods=["GET"])
@token_required
@role_required("customer", "admin")
def get_complaints():
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = ComplaintRepository()
    service = ComplaintService(repository)

    complaints = service.list_for_user(
        user_id,
        is_admin
    )

    return jsonify([
        complaint_to_dict(complaint)
        for complaint in complaints
    ]), 200


@bp.route("/<complaint_id>", methods=["GET"])
@token_required
@role_required("customer", "admin")
def get_complaint(complaint_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = ComplaintRepository()
    service = ComplaintService(repository)

    complaint, error = service.get_by_id_for_user(
        complaint_id,
        user_id,
        is_admin
    )

    if error:
        status_code = 404 if error == "Complaint not found" else 403
        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        complaint_to_dict(complaint)
    ), 200


@bp.route("", methods=["POST"])
@token_required
@role_required("customer")
def create_complaint():
    user_id = request.user_id
    data = request.get_json() or {}

    if not data.get("type"):
        return jsonify({
            "message": "type is required"
        }), 400

    if not data.get("description"):
        return jsonify({
            "message": "description is required"
        }), 400

    repository = ComplaintRepository()
    service = ComplaintService(repository)

    complaint, error = service.create(
        user_id,
        data
    )

    if error:
        return jsonify({
            "message": error
        }), 400

    return jsonify(
        complaint_to_dict(complaint)
    ), 201


@bp.route("/<complaint_id>", methods=["PUT"])
@token_required
@role_required("customer", "admin")
def update_complaint(complaint_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"
    data = request.get_json() or {}

    repository = ComplaintRepository()
    service = ComplaintService(repository)

    complaint, error = service.update(
        complaint_id,
        user_id,
        data,
        is_admin
    )

    if error:
        status_code = 404 if error == "Complaint not found" else 403
        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        complaint_to_dict(complaint)
    ), 200


@bp.route("/<complaint_id>", methods=["DELETE"])
@token_required
@role_required("customer", "admin")
def delete_complaint(complaint_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = ComplaintRepository()
    service = ComplaintService(repository)

    success, error = service.delete(
        complaint_id,
        user_id,
        is_admin
    )

    if error:
        status_code = 404 if error == "Complaint not found" else 403
        return jsonify({
            "message": error
        }), status_code

    return jsonify({
        "message": "Complaint deleted successfully"
    }), 200