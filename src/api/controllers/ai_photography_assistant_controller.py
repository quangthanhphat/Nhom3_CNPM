from flask import Blueprint, request, jsonify

from api.middleware import token_required, role_required

from infrastructure.repositories.knowledge_base_repository import (
    KnowledgeBaseRepository
)

from services.ai_photography_assistant_service import (
    AIPhotographyAssistantService
)


bp = Blueprint(
    "ai_photography_assistant",
    __name__,
    url_prefix="/api/ai/assistant"
)


@bp.route("", methods=["POST"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "delivery_partner",
    "admin"
)
def ask_assistant():
    data = request.get_json() or {}

    question = data.get("question")

    if not question:
        return jsonify({
            "message": "question is required"
        }), 400

    repository = KnowledgeBaseRepository()

    service = AIPhotographyAssistantService(
        repository
    )

    result = service.ask(question)

    return jsonify(result), 200