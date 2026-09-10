from flask import Blueprint, request, jsonify

from api.middleware import token_required, role_required
from infrastructure.repositories.support_repository import SupportRepository
from services.support_service import SupportService


bp = Blueprint(
    "support",
    __name__,
    url_prefix="/api/support"
)


def support_to_dict(support):
    return {
        "id": str(support.id),
        "user_id": str(support.user_id),
        "subject": support.subject,
        "message": support.message,
        "reply": support.reply,
        "status": support.status,
        "created_at": (
            support.created_at.isoformat()
            if support.created_at
            else None
        ),
        "updated_at": (
            support.updated_at.isoformat()
            if support.updated_at
            else None
        )
    }


@bp.route("", methods=["GET"])
@token_required
@role_required("film_lab_owner", "admin")
def get_support_tickets():
    user_id = request.user.get("user_id")
    role = request.user.get("role")

    repository = SupportRepository()
    service = SupportService(repository)

    tickets = service.list_for_user(user_id, role)

    return jsonify([
        support_to_dict(ticket)
        for ticket in tickets
    ]), 200


@bp.route("/<support_id>", methods=["GET"])
@token_required
@role_required("film_lab_owner", "admin")
def get_support_ticket(support_id):
    user_id = request.user.get("user_id")
    role = request.user.get("role")

    repository = SupportRepository()
    service = SupportService(repository)

    support, error = service.get_by_id_for_user(
        support_id,
        user_id,
        role
    )

    if error:
        status_code = 404 if error == "not_found" else 403

        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        support_to_dict(support)
    ), 200


@bp.route("", methods=["POST"])
@token_required
@role_required("film_lab_owner")
def create_support_ticket():
    user_id = request.user.get("user_id")

    data = request.get_json() or {}

    if not data.get("subject"):
        return jsonify({
            "message": "subject is required"
        }), 400

    if not data.get("message"):
        return jsonify({
            "message": "message is required"
        }), 400

    repository = SupportRepository()
    service = SupportService(repository)

    support, error = service.create(
        user_id,
        data
    )

    if error:
        return jsonify({
            "message": error
        }), 400

    return jsonify(
        support_to_dict(support)
    ), 201


@bp.route("/<support_id>/reply", methods=["PUT"])
@token_required
@role_required("admin")
def reply_support_ticket(support_id):
    user_id = request.user.get("user_id")
    role = request.user.get("role")

    data = request.get_json() or {}

    if not data.get("reply"):
        return jsonify({
            "message": "reply is required"
        }), 400

    repository = SupportRepository()
    service = SupportService(repository)

    support, error = service.reply(
        support_id,
        data.get("reply"),
        user_id,
        role
    )

    if error:
        status_code = 404 if error == "not_found" else 403

        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        support_to_dict(support)
    ), 200


@bp.route("/<support_id>/close", methods=["PUT"])
@token_required
@role_required("admin")
def close_support_ticket(support_id):
    user_id = request.user.get("user_id")
    role = request.user.get("role")

    repository = SupportRepository()
    service = SupportService(repository)

    support, error = service.close(
        support_id,
        user_id,
        role
    )

    if error:
        status_code = 404 if error == "not_found" else 403

        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        support_to_dict(support)
    ), 200


@bp.route("/<support_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_support_ticket(support_id):
    user_id = request.user.get("user_id")
    role = request.user.get("role")

    repository = SupportRepository()
    service = SupportService(repository)

    success, error = service.delete(
        support_id,
        user_id,
        role
    )

    if error:
        status_code = 404 if error == "not_found" else 403

        return jsonify({
            "message": error
        }), status_code

    return jsonify({
        "message": "Support ticket deleted successfully"
    }), 200