from flask import Blueprint, jsonify, request

from services.delivery_service import DeliveryService
from api.middleware import token_required, role_required


bp = Blueprint(
    'delivery',
    __name__,
    url_prefix='/deliveries'
)

delivery_service = DeliveryService()


# =========================
# GET ALL DELIVERIES
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'delivery_partner',
    'admin'
)
def get_all_deliveries():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deliveries = delivery_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for delivery in deliveries:
        result.append({
            'id': str(delivery.id),
            'order_id': str(delivery.order_id),
            'delivery_partner_id': (
                str(delivery.delivery_partner_id)
                if delivery.delivery_partner_id
                else None
            ),
            'delivery_type': delivery.delivery_type,
            'pickup_address': delivery.pickup_address,
            'destination_address': delivery.destination_address,
            'status': delivery.status,
            'external_delivery_reference': (
                delivery.external_delivery_reference
            )
        })

    return jsonify(result), 200


# =========================
# CREATE DELIVERY
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def create_delivery():
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    delivery, error = delivery_service.create(
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'order_not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only create delivery '
                'for orders of your own film lab'
            )
        }), 403

    return jsonify({
        'message': 'Delivery created successfully',
        'delivery': {
            'id': str(delivery.id),
            'order_id': str(delivery.order_id),
            'delivery_partner_id': (
                str(delivery.delivery_partner_id)
                if delivery.delivery_partner_id
                else None
            ),
            'delivery_type': delivery.delivery_type,
            'pickup_address': delivery.pickup_address,
            'destination_address': delivery.destination_address,
            'status': delivery.status,
            'external_delivery_reference': (
                delivery.external_delivery_reference
            )
        }
    }), 201


# =========================
# GET DELIVERY BY ID
# =========================

@bp.route('/<uuid:delivery_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'delivery_partner',
    'admin'
)
def get_delivery(delivery_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    delivery, error = delivery_service.get_by_id_for_user(
        delivery_id=delivery_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Delivery not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this delivery'
            )
        }), 403

    return jsonify({
        'id': str(delivery.id),
        'order_id': str(delivery.order_id),
        'delivery_partner_id': (
            str(delivery.delivery_partner_id)
            if delivery.delivery_partner_id
            else None
        ),
        'delivery_type': delivery.delivery_type,
        'pickup_address': delivery.pickup_address,
        'destination_address': delivery.destination_address,
        'status': delivery.status,
        'external_delivery_reference': (
            delivery.external_delivery_reference
        )
    }), 200


# =========================
# UPDATE DELIVERY
# =========================

@bp.route('/<uuid:delivery_id>', methods=['PUT'])
@token_required
@role_required(
    'film_lab_owner',
    'delivery_partner',
    'admin'
)
def update_delivery(delivery_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    delivery, error = delivery_service.update(
        delivery_id=delivery_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Delivery not found'
        }), 404

    if error == 'order_not_found':
        return jsonify({
            'message': 'Order not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to update this delivery'
            )
        }), 403

    return jsonify({
        'message': 'Delivery updated successfully',
        'delivery': {
            'id': str(delivery.id),
            'order_id': str(delivery.order_id),
            'delivery_partner_id': (
                str(delivery.delivery_partner_id)
                if delivery.delivery_partner_id
                else None
            ),
            'delivery_type': delivery.delivery_type,
            'pickup_address': delivery.pickup_address,
            'destination_address': delivery.destination_address,
            'status': delivery.status,
            'external_delivery_reference': (
                delivery.external_delivery_reference
            )
        }
    }), 200


# =========================
# DELETE DELIVERY
# =========================

@bp.route('/<uuid:delivery_id>', methods=['DELETE'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def delete_delivery(delivery_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = delivery_service.delete(
        delivery_id=delivery_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Delivery not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this delivery'
            )
        }), 403

    return jsonify({
        'message': 'Delivery deleted successfully'
    }), 200