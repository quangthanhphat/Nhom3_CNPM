from flask import Blueprint, jsonify, request

from services.marketplace_transaction_service import (
    MarketplaceTransactionService
)
from api.middleware import token_required, role_required


bp = Blueprint(
    'marketplace_transaction',
    __name__,
    url_prefix='/marketplace-transactions'
)

marketplace_transaction_service = MarketplaceTransactionService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_all_transactions():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    transactions = marketplace_transaction_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for transaction in transactions:
        result.append({
            'id': str(transaction.id),
            'listing_id': str(transaction.listing_id),
            'buyer_id': str(transaction.buyer_id),
            'quantity': transaction.quantity,
            'total_amount': transaction.total_amount,
            'status': transaction.status,
            'created_at': transaction.created_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert'
)
def create_transaction():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('listing_id'):
        return jsonify({
            'message': 'listing_id is required'
        }), 400

    quantity = data.get('quantity', 1)

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({
            'message': 'quantity must be a positive integer'
        }), 400

    buyer_id = request.user.get('user_id')

    transaction, error = marketplace_transaction_service.create(
        buyer_id=buyer_id,
        data=data
    )

    if error == 'listing_not_found':
        return jsonify({
            'message': 'Marketplace listing not found'
        }), 404

    if error == 'own_listing':
        return jsonify({
            'message': 'You cannot buy your own listing'
        }), 400

    if error == 'sold_out':
        return jsonify({
            'message': 'This listing is sold out'
        }), 400

    if error == 'insufficient_quantity':
        return jsonify({
            'message': 'Insufficient quantity'
        }), 400

    if error == 'invalid_quantity':
        return jsonify({
            'message': 'Invalid quantity'
        }), 400

    return jsonify({
        'message': 'Marketplace transaction created successfully',
        'transaction': {
            'id': str(transaction.id),
            'listing_id': str(transaction.listing_id),
            'buyer_id': str(transaction.buyer_id),
            'quantity': transaction.quantity,
            'total_amount': transaction.total_amount,
            'status': transaction.status,
            'created_at': transaction.created_at
        }
    }), 201


@bp.route('/<uuid:transaction_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_transaction(transaction_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    transaction, error = (
        marketplace_transaction_service.get_by_id_for_user(
            transaction_id=transaction_id,
            user_id=user_id,
            role=role
        )
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace transaction not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this transaction'
            )
        }), 403

    return jsonify({
        'id': str(transaction.id),
        'listing_id': str(transaction.listing_id),
        'buyer_id': str(transaction.buyer_id),
        'quantity': transaction.quantity,
        'total_amount': transaction.total_amount,
        'status': transaction.status,
        'created_at': transaction.created_at
    }), 200


@bp.route('/<uuid:transaction_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def delete_transaction(transaction_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = marketplace_transaction_service.delete(
        transaction_id=transaction_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace transaction not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this transaction'
            )
        }), 403

    return jsonify({
        'message': 'Marketplace transaction deleted successfully'
    }), 200