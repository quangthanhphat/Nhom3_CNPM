from flask import Blueprint, jsonify, request

from services.marketplace_message_service import (
    MarketplaceMessageService
)
from api.middleware import token_required, role_required


bp = Blueprint(
    'marketplace_message',
    __name__,
    url_prefix='/marketplace-messages'
)

marketplace_message_service = MarketplaceMessageService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_all_messages():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    messages = marketplace_message_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for message in messages:
        result.append({
            'id': str(message.id),
            'listing_id': str(message.listing_id),
            'sender_id': str(message.sender_id),
            'receiver_id': str(message.receiver_id),
            'content': message.content,
            'created_at': message.created_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert'
)
def create_message():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('listing_id'):
        return jsonify({
            'message': 'listing_id is required'
        }), 400

    if not data.get('receiver_id'):
        return jsonify({
            'message': 'receiver_id is required'
        }), 400

    if not data.get('content'):
        return jsonify({
            'message': 'content is required'
        }), 400

    sender_id = request.user.get('user_id')

    message, error = marketplace_message_service.create(
        sender_id=sender_id,
        data=data
    )

    if error == 'listing_not_found':
        return jsonify({
            'message': 'Marketplace listing not found'
        }), 404

    if error == 'invalid_receiver':
        return jsonify({
            'message': 'Invalid receiver'
        }), 400

    if error == 'forbidden':
        return jsonify({
            'message': (
                'Only the buyer and seller '
                'can exchange messages'
            )
        }), 403

    return jsonify({
        'message': 'Marketplace message created successfully',
        'message_data': {
            'id': str(message.id),
            'listing_id': str(message.listing_id),
            'sender_id': str(message.sender_id),
            'receiver_id': str(message.receiver_id),
            'content': message.content,
            'created_at': message.created_at
        }
    }), 201


@bp.route('/<uuid:message_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_message(message_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    message, error = (
        marketplace_message_service.get_by_id_for_user(
            message_id=message_id,
            user_id=user_id,
            role=role
        )
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace message not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this message'
            )
        }), 403

    return jsonify({
        'id': str(message.id),
        'listing_id': str(message.listing_id),
        'sender_id': str(message.sender_id),
        'receiver_id': str(message.receiver_id),
        'content': message.content,
        'created_at': message.created_at
    }), 200


@bp.route('/<uuid:message_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def delete_message(message_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = marketplace_message_service.delete(
        message_id=message_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace message not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only delete '
                'your own conversation messages'
            )
        }), 403

    return jsonify({
        'message': 'Marketplace message deleted successfully'
    }), 200