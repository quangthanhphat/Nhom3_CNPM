from flask import Blueprint, jsonify, request

from services.order_service import OrderService
from api.middleware import token_required, role_required


bp = Blueprint(
    'order',
    __name__,
    url_prefix='/orders'
)

order_service = OrderService()


# =========================
# GET ALL ORDERS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_all_orders():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    orders = order_service.list_for_user(
        user_id=user_id,
        role=role
    )

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


# =========================
# CREATE ORDER
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer'
)
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


# =========================
# GET ORDER BY ID
# =========================

@bp.route('/<uuid:order_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def get_order(order_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    order, error = order_service.get_by_id_for_user(
        order_id=order_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You do not have permission to view this order'
        }), 403

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


# =========================
# UPDATE ORDER
# =========================

@bp.route('/<uuid:order_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def update_order(order_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    order, error = order_service.update(
        order_id=order_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You do not have permission to update this order'
        }), 403

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


# =========================
# DELETE ORDER
# =========================

@bp.route('/<uuid:order_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'admin'
)
def delete_order(order_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = order_service.delete(
        order_id=order_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You do not have permission to delete this order'
        }), 403

    return jsonify({
        'message': 'Order deleted successfully'
    }), 200