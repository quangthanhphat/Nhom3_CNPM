from flask import Blueprint, jsonify, request

from services.order_service import OrderService
from api.middleware import token_required, role_required


bp = Blueprint(
    'order',
    __name__,
    url_prefix='/orders'
)

order_service = OrderService()


def _serialize_order(order):
    return {
        'id': str(order.id),
        'customer_id': str(order.customer_id),
        'film_lab_id': str(order.film_lab_id),
        'service_id': str(order.service_id),
        'film_type_id': str(order.film_type_id),

        'quantity': order.quantity,

        'processing_options': order.processing_options,
        'scanning_quality': order.scanning_quality,
        'printing_requirements': order.printing_requirements,
        'additional_requests': order.additional_requests,

        'delivery_type': order.delivery_type,

        'status': order.status,
        'total_amount': order.total_amount,
        'notes': order.notes,

        'created_at': (
            order.created_at.isoformat()
            if order.created_at
            else None
        ),
        'updated_at': (
            order.updated_at.isoformat()
            if order.updated_at
            else None
        )
    }


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

    result = [
        _serialize_order(order)
        for order in orders
    ]

    return jsonify(result), 200


# =========================
# CREATE ORDER REQUEST
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer'
)
def create_order():
    data = request.get_json() or {}

    customer_id = request.user.get('user_id')

    order = order_service.create(
        customer_id=customer_id,
        data=data
    )

    return jsonify({
        'message': 'Order request created successfully',
        'order': _serialize_order(order)
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

    return jsonify(
        _serialize_order(order)
    ), 200


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
    data = request.get_json() or {}

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    # Owner không được tự chuyển Order sang processing.
    # Order chỉ chuyển sang processing sau khi payment thành công.
    if (
        role == 'film_lab_owner'
        and data.get('status') == 'processing'
    ):
        return jsonify({
            'message': (
                'Order can only move to processing '
                'after successful payment'
            )
        }), 400

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
            'message': (
                'You do not have permission '
                'to update this order'
            )
        }), 403

    return jsonify({
        'message': 'Order updated successfully',
        'order': _serialize_order(order)
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
            'message': (
                'You do not have permission '
                'to delete this order'
            )
        }), 403

    return jsonify({
        'message': 'Order deleted successfully'
    }), 200