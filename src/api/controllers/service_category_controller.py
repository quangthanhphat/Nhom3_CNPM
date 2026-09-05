from flask import Blueprint, jsonify, request

from services.service_category_service import ServiceCategoryService
from api.middleware import token_required


bp = Blueprint(
    'service_category',
    __name__,
    url_prefix='/service-categories'
)

service_category_service = ServiceCategoryService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_categories():
    categories = service_category_service.list_all()

    result = []

    for category in categories:
        result.append({
            'id': str(category.id),
            'name': category.name,
            'description': category.description
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
def create_category():
    data = request.get_json()

    category = service_category_service.create(data)

    return jsonify({
        'message': 'Service category created successfully',
        'category': {
            'id': str(category.id),
            'name': category.name,
            'description': category.description
        }
    }), 201


@bp.route('/<uuid:category_id>', methods=['GET'])
@token_required
def get_category(category_id):
    category = service_category_service.get_by_id(category_id)

    if not category:
        return jsonify({
            'message': 'Service category not found'
        }), 404

    return jsonify({
        'id': str(category.id),
        'name': category.name,
        'description': category.description
    }), 200


@bp.route('/<uuid:category_id>', methods=['PUT'])
@token_required
def update_category(category_id):
    data = request.get_json()

    category = service_category_service.update(
        category_id=category_id,
        data=data
    )

    if not category:
        return jsonify({
            'message': 'Service category not found'
        }), 404

    return jsonify({
        'message': 'Service category updated successfully',
        'category': {
            'id': str(category.id),
            'name': category.name,
            'description': category.description
        }
    }), 200


@bp.route('/<uuid:category_id>', methods=['DELETE'])
@token_required
def delete_category(category_id):
    deleted = service_category_service.delete(category_id)

    if not deleted:
        return jsonify({
            'message': 'Service category not found'
        }), 404

    return jsonify({
        'message': 'Service category deleted successfully'
    }), 200