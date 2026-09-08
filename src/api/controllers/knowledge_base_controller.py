from flask import Blueprint, request, jsonify

from api.middleware import token_required, role_required
from infrastructure.models.generated_models import KnowledgeBase

from infrastructure.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository
)
from services.knowledge_base_service import KnowledgeBaseService


bp = Blueprint(
    "knowledge_base",
    __name__,
    url_prefix="/api/knowledge-base"
)


def knowledge_to_dict(knowledge):
    return {
        "id": str(knowledge.id),
        "author_id": str(knowledge.author_id),
        "title": knowledge.title,
        "content": knowledge.content,
        "status": knowledge.status,
        "created_at": (
            knowledge.created_at.isoformat()
            if knowledge.created_at
            else None
        ),
        "post_id": (
            str(knowledge.post_id)
            if knowledge.post_id
            else None
        ),
        "updated_at": (
            knowledge.updated_at.isoformat()
            if knowledge.updated_at
            else None
        )
    }


@bp.route("", methods=["GET"])
@token_required
@role_required(
    "customer",
    "photography_expert",
    "admin"
)
def get_knowledge_base():
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = KnowledgeBaseRepository()
    service = KnowledgeBaseService(repository)

    knowledge_list = service.list_for_user(
        user_id,
        is_admin
    )

    return jsonify([
        knowledge_to_dict(knowledge)
        for knowledge in knowledge_list
    ]), 200


@bp.route("/<knowledge_id>", methods=["GET"])
@token_required
@role_required(
    "customer",
    "photography_expert",
    "admin"
)
def get_knowledge(knowledge_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = KnowledgeBaseRepository()
    service = KnowledgeBaseService(repository)

    knowledge, error = service.get_by_id_for_user(
        knowledge_id,
        user_id,
        is_admin
    )

    if error:
        status_code = (
            404
            if error == "Knowledge base entry not found"
            else 403
        )

        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        knowledge_to_dict(knowledge)
    ), 200


@bp.route("", methods=["POST"])
@token_required
@role_required("photography_expert")
def create_knowledge():
    user_id = request.user_id
    data = request.get_json() or {}

    if not data.get("title"):
        return jsonify({
            "message": "title is required"
        }), 400

    if not data.get("content"):
        return jsonify({
            "message": "content is required"
        }), 400

    repository = KnowledgeBaseRepository()
    service = KnowledgeBaseService(repository)

    knowledge, error = service.create(
        user_id,
        data
    )

    if error:
        return jsonify({
            "message": error
        }), 400

    return jsonify(
        knowledge_to_dict(knowledge)
    ), 201


@bp.route("/<knowledge_id>", methods=["PUT"])
@token_required
@role_required(
    "photography_expert",
    "admin"
)
def update_knowledge(knowledge_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"
    data = request.get_json() or {}

    repository = KnowledgeBaseRepository()
    service = KnowledgeBaseService(repository)

    knowledge, error = service.update(
        knowledge_id,
        user_id,
        data,
        is_admin
    )

    if error:
        status_code = (
            404
            if error == "Knowledge base entry not found"
            else 403
        )

        return jsonify({
            "message": error
        }), status_code

    return jsonify(
        knowledge_to_dict(knowledge)
    ), 200


@bp.route("/<knowledge_id>", methods=["DELETE"])
@token_required
@role_required(
    "photography_expert",
    "admin"
)
def delete_knowledge(knowledge_id):
    user_id = request.user_id
    is_admin = request.user_role == "admin"

    repository = KnowledgeBaseRepository()
    service = KnowledgeBaseService(repository)

    success, error = service.delete(
        knowledge_id,
        user_id,
        is_admin
    )

    if error:
        status_code = (
            404
            if error == "Knowledge base entry not found"
            else 403
        )

        return jsonify({
            "message": error
        }), status_code

    return jsonify({
        "message": "Knowledge base entry deleted successfully"
    }), 200