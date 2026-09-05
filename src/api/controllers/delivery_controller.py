from flask import Blueprint, jsonify, request

from services.delivery_service import DeliveryService
from api.middleware import token_required


bp = Blueprint(
    'delivery',
    __name__,
    url_prefix='/deliveries'
)

delivery_service = DeliveryService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_deliveries():
    deliveries = delivery_service.list_all()

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


@bp.route('/', methods=['POST'])
@token_required
def create_delivery():
    data = request.get_json()

    delivery = delivery_service.create(data)

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


@bp.route('/<uuid:delivery_id>', methods=['GET'])
@token_required
def get_delivery(delivery_id):
    delivery = delivery_service.get_by_id(delivery_id)

    if not delivery:
        return jsonify({
            'message': 'Delivery not found'
        }), 404

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


@bp.route('/<uuid:delivery_id>', methods=['PUT'])
@token_required
def update_delivery(delivery_id):
    data = request.get_json()

    delivery = delivery_service.update(
        delivery_id=delivery_id,
        data=data
    )

    if not delivery:
        return jsonify({
            'message': 'Delivery not found'
        }), 404

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


@bp.route('/<uuid:delivery_id>', methods=['DELETE'])
@token_required
def delete_delivery(delivery_id):
    deleted = delivery_service.delete(delivery_id)

    if not deleted:
        return jsonify({
            'message': 'Delivery not found'
        }), 404

    return jsonify({
        'message': 'Delivery deleted successfully'
    }), 200