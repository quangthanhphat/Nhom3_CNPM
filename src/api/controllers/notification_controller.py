from flask import Blueprint, jsonify, request

from infrastructure.repositories.notification_repository import NotificationRepository
from services.notification_service import NotificationService
from api.middleware import token_required, role_required


bp = Blueprint("notification", __name__, url_prefix="/api/notifications")


def get_user_id():
    return getattr(request, "user_id", None)


def get_is_admin():
    return getattr(request, "role", None) == "admin"


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "delivery_partner",
    "admin"
)
def get_notifications():
    repository = NotificationRepository()
    service = NotificationService(repository)

    user_id = get_user_id()
    is_admin = get_is_admin()

    notifications = service.list_for_user(
        user_id=user_id,
        is_admin=is_admin
    )

    return jsonify([
        {
            "id": str(notification.id),
            "user_id": str(notification.user_id),
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat()
            if notification.created_at else None
        }
        for notification in notifications
    ]), 200


@bp.route("/<uuid:notification_id>", methods=["GET"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "delivery_partner",
    "admin"
)
def get_notification(notification_id):
    repository = NotificationRepository()
    service = NotificationService(repository)

    notification, error = service.get_by_id_for_user(
        notification_id=notification_id,
        user_id=get_user_id(),
        is_admin=get_is_admin()
    )

    if error == "Forbidden":
        return jsonify({"message": error}), 403

    if error:
        return jsonify({"message": error}), 404

    return jsonify({
        "id": str(notification.id),
        "user_id": str(notification.user_id),
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat()
        if notification.created_at else None
    }), 200


@bp.route("", methods=["POST"])
@bp.route("/", methods=["POST"])
@token_required
@role_required("admin")
def create_notification():
    repository = NotificationRepository()
    service = NotificationService(repository)

    data = request.get_json() or {}

    notification, error = service.create(data)

    if error:
        return jsonify({"message": error}), 400

    return jsonify({
        "id": str(notification.id),
        "user_id": str(notification.user_id),
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat()
        if notification.created_at else None
    }), 201


@bp.route("/<uuid:notification_id>/read", methods=["PUT"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "delivery_partner",
    "admin"
)
def mark_notification_read(notification_id):
    repository = NotificationRepository()
    service = NotificationService(repository)

    notification, error = service.mark_as_read(
        notification_id=notification_id,
        user_id=get_user_id(),
        is_admin=get_is_admin()
    )

    if error == "Forbidden":
        return jsonify({"message": error}), 403

    if error:
        return jsonify({"message": error}), 404

    return jsonify({
        "message": "Notification marked as read",
        "id": str(notification.id)
    }), 200


@bp.route("/<uuid:notification_id>", methods=["DELETE"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "delivery_partner",
    "admin"
)
def delete_notification(notification_id):
    repository = NotificationRepository()
    service = NotificationService(repository)

    success, error = service.delete(
        notification_id=notification_id,
        user_id=get_user_id(),
        is_admin=get_is_admin()
    )

    if error == "Forbidden":
        return jsonify({"message": error}), 403

    if error:
        return jsonify({"message": error}), 404

    return jsonify({
        "message": "Notification deleted successfully"
    }), 200