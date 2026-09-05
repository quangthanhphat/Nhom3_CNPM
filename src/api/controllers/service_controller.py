from flask import Blueprint, jsonify, request
from services.service_service import ServiceService
from api.middleware import token_required


bp = Blueprint(
    'service',
    __name__,
    url_prefix='/services'
)

service_service = ServiceService()


@bp.route('/', methods=['GET'])
@token_required
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
            'turnaround_time': service.turnaround_time,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
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
            'turnaround_time': service.turnaround_time,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        }
    }), 201


@bp.route('/<uuid:service_id>', methods=['GET'])
@token_required
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
        'turnaround_time': service.turnaround_time,
        'processing_capacity': service.processing_capacity,
        'supported_film_formats': service.supported_film_formats,
        'processing_options': service.processing_options,
        'scanning_quality': service.scanning_quality,
        'printing_options': service.printing_options,
        'specialized_techniques': service.specialized_techniques,
        'status': service.status
    }), 200


@bp.route('/<uuid:service_id>', methods=['PUT'])
@token_required
def update_service(service_id):
    data = request.get_json()

    service = service_service.update(
        service_id=service_id,
        data=data
    )

    if not service:
        return jsonify({
            'message': 'Service not found'
        }), 404

    return jsonify({
        'message': 'Service updated successfully',
        'service': {
            'id': str(service.id),
            'film_lab_id': str(service.film_lab_id),
            'category_id': str(service.category_id),
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'turnaround_time': service.turnaround_time,
            'processing_capacity': service.processing_capacity,
            'supported_film_formats': service.supported_film_formats,
            'processing_options': service.processing_options,
            'scanning_quality': service.scanning_quality,
            'printing_options': service.printing_options,
            'specialized_techniques': service.specialized_techniques,
            'status': service.status
        }
    }), 200


@bp.route('/<uuid:service_id>', methods=['DELETE'])
@token_required
def delete_service(service_id):
    deleted = service_service.delete(service_id)

    if not deleted:
        return jsonify({
            'message': 'Service not found'
        }), 404

    return jsonify({
        'message': 'Service deleted successfully'
    }), 200