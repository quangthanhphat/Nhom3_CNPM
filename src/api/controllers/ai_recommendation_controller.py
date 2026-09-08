from flask import Blueprint, request, jsonify

from api.middleware import token_required, role_required

from infrastructure.repositories.service_repository import ServiceRepository
from services.ai_recommendation_service import AIRecommendationService


bp = Blueprint(
    "ai_recommendation",
    __name__,
    url_prefix="/api/ai/recommendations"
)


def service_to_dict(service, score, reasons):
    return {
        "id": str(service.id),
        "film_lab_id": str(service.film_lab_id),
        "category_id": str(service.category_id),
        "name": service.name,
        "description": service.description,
        "price": float(service.price),
        "turnaround_time_min": service.turnaround_time_min,
        "turnaround_time_max": service.turnaround_time_max,
        "supported_film_formats": service.supported_film_formats,
        "processing_options": service.processing_options,
        "scanning_quality": service.scanning_quality,
        "printing_options": service.printing_options,
        "specialized_techniques": service.specialized_techniques,
        "score": score,
        "reasons": reasons
    }


@bp.route("", methods=["POST"])
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "photography_expert",
    "admin"
)
def recommend_services():
    data = request.get_json() or {}

    repository = ServiceRepository()
    service = AIRecommendationService(repository)

    recommendations = service.recommend(data)

    return jsonify([
        service_to_dict(
            item["service"],
            item["score"],
            item["reasons"]
        )
        for item in recommendations
    ]), 200