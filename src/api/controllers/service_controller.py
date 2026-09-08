from flask import Blueprint, jsonify, request

from services.service_service import ServiceService
from api.middleware import token_required, role_required


bp = Blueprint(
    'service',
    __name__,
    url_prefix='/services'
)

service_service = ServiceService()


# =========================
# GET ALL SERVICES
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'film_lab_owner',
    'admin'
)
def get_all_services():
    services = service_service.list_all()

    result = []

    for service in services:
        result.append({
            'id': str(service.id),
            'film_lab_id': str(service.film_lab_id),
            'category_id': str(service.category_id),
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'turnaround_time_min': service.turnaround_time_min,
            'turnaround_time_max': service.turnaround_time_max,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        })

    return jsonify(result), 200


# =========================
# CREATE SERVICE
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def create_service():
    data = request.get_json()

    service = service_service.create(data)

    return jsonify({
        'message': 'Service created successfully',
        'service': {
            'id': str(service.id),
            'film_lab_id': str(service.film_lab_id),
            'category_id': str(service.category_id),
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'turnaround_time_min': service.turnaround_time_min,
            'turnaround_time_max': service.turnaround_time_max,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        }
    }), 201


# =========================
# GET SERVICE BY ID
# =========================

@bp.route('/<uuid:service_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'film_lab_owner',
    'admin'
)
def get_service(service_id):
    service = service_service.get_by_id(service_id)

    if not service:
        return jsonify({
            'message': 'Service not found'
        }), 404

    return jsonify({
        'id': str(service.id),
        'film_lab_id': str(service.film_lab_id),
        'category_id': str(service.category_id),
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'turnaround_time_min': service.turnaround_time_min,
        'turnaround_time_max': service.turnaround_time_max,
        'processing_capacity': service.processing_capacity,
        'supported_film_formats': service.supported_film_formats,
        'processing_options': service.processing_options,
        'scanning_quality': service.scanning_quality,
        'printing_options': service.printing_options,
        'specialized_techniques': service.specialized_techniques,
        'status': service.status
    }), 200


# =========================
# UPDATE SERVICE
# =========================

@bp.route('/<uuid:service_id>', methods=['PUT'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def update_service(service_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    is_admin = request.user.get('role') == 'admin'

    service, error = service_service.update(
        service_id=service_id,
        data=data,
        user_id=user_id,
        is_admin=is_admin
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Service not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only update services of your own film lab'
        }), 403

    return jsonify({
        'message': 'Service updated successfully',
        'service': {
            'id': str(service.id),
            'film_lab_id': str(service.film_lab_id),
            'category_id': str(service.category_id),
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'turnaround_time_min': service.turnaround_time_min,
            'turnaround_time_max': service.turnaround_time_max,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        }
    }), 200


# =========================
# DELETE SERVICE
# =========================

@bp.route('/<uuid:service_id>', methods=['DELETE'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def delete_service(service_id):
    user_id = request.user.get('user_id')
    is_admin = request.user.get('role') == 'admin'

    deleted, error = service_service.delete(
        service_id=service_id,
        user_id=user_id,
        is_admin=is_admin
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Service not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only delete services of your own film lab'
        }), 403

    return jsonify({
        'message': 'Service deleted successfully'
    }), 200