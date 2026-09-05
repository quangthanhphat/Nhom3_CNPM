from flask import Blueprint, jsonify, request

from services.order_service import OrderService
from api.middleware import token_required


bp = Blueprint(
    'order',
    __name__,
    url_prefix='/orders'
)

order_service = OrderService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_orders():
    orders = order_service.list_all()

    result = []

    for order in orders:
        result.append({
            'id': str(order.id),
            'customer_id': str(order.customer_id),
            'film_lab_id': str(order.film_lab_id),
            'service_id': str(order.service_id),
            'film_type_id': str(order.film_type_id),
            'processing_options': order.processing_options,
            'scanning_quality': order.scanning_quality,
            'printing_requirements': order.printing_requirements,
            'additional_requests': order.additional_requests,
            'status': order.status,
            'total_amount': order.total_amount,
            'notes': order.notes
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
def create_order():
    data = request.get_json()
    customer_id = request.user.get('user_id')

    order = order_service.create(
        customer_id=customer_id,
        data=data
    )

    return jsonify({
        'message': 'Order created successfully',
        'order': {
            'id': str(order.id),
            'customer_id': str(order.customer_id),
            'film_lab_id': str(order.film_lab_id),
            'service_id': str(order.service_id),
            'film_type_id': str(order.film_type_id),
            'processing_options': order.processing_options,
            'scanning_quality': order.scanning_quality,
            'printing_requirements': order.printing_requirements,
            'additional_requests': order.additional_requests,
            'status': order.status,
            'total_amount': order.total_amount,
            'notes': order.notes
        }
    }), 201


@bp.route('/<uuid:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    order = order_service.get_by_id(order_id)

    if not order:
        return jsonify({
            'message': 'Order not found'
        }), 404

    return jsonify({
        'id': str(order.id),
        'customer_id': str(order.customer_id),
        'film_lab_id': str(order.film_lab_id),
        'service_id': str(order.service_id),
        'film_type_id': str(order.film_type_id),
        'processing_options': order.processing_options,
        'scanning_quality': order.scanning_quality,
        'printing_requirements': order.printing_requirements,
        'additional_requests': order.additional_requests,
        'status': order.status,
        'total_amount': order.total_amount,
        'notes': order.notes
    }), 200


@bp.route('/<uuid:order_id>', methods=['PUT'])
@token_required
def update_order(order_id):
    data = request.get_json()

    order = order_service.update(
        order_id=order_id,
        data=data
    )

    if not order:
        return jsonify({
            'message': 'Order not found'
        }), 404

    return jsonify({
        'message': 'Order updated successfully',
        'order': {
            'id': str(order.id),
            'customer_id': str(order.customer_id),
            'film_lab_id': str(order.film_lab_id),
            'service_id': str(order.service_id),
            'film_type_id': str(order.film_type_id),
            'processing_options': order.processing_options,
            'scanning_quality': order.scanning_quality,
            'printing_requirements': order.printing_requirements,
            'additional_requests': order.additional_requests,
            'status': order.status,
            'total_amount': order.total_amount,
            'notes': order.notes
        }
    }), 200


@bp.route('/<uuid:order_id>', methods=['DELETE'])
@token_required
def delete_order(order_id):
    deleted = order_service.delete(order_id)

    if not deleted:
        return jsonify({
            'message': 'Order not found'
        }), 404

    return jsonify({
        'message': 'Order deleted successfully'
    }), 200