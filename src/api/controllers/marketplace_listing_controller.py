from flask import Blueprint, jsonify, request

from services.marketplace_listing_service import MarketplaceListingService
from api.middleware import token_required, role_required


bp = Blueprint(
    'marketplace_listing',
    __name__,
    url_prefix='/marketplace-listings'
)

marketplace_listing_service = MarketplaceListingService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_all_listings():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    listings = marketplace_listing_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for listing in listings:
        result.append({
            'id': str(listing.id),
            'seller_id': str(listing.seller_id),
            'category': listing.category,
            'title': listing.title,
            'description': listing.description,
            'price': listing.price,
            'quantity': listing.quantity,
            'status': listing.status,
            'created_at': listing.created_at,
            'updated_at': listing.updated_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert'
)
def create_listing():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('title'):
        return jsonify({
            'message': 'title is required'
        }), 400

    if data.get('price') is None:
        return jsonify({
            'message': 'price is required'
        }), 400

    seller_id = request.user.get('user_id')

    listing = marketplace_listing_service.create(
        seller_id=seller_id,
        data=data
    )

    return jsonify({
        'message': 'Marketplace listing created successfully',
        'listing': {
            'id': str(listing.id),
            'seller_id': str(listing.seller_id),
            'category': listing.category,
            'title': listing.title,
            'description': listing.description,
            'price': listing.price,
            'quantity': listing.quantity,
            'status': listing.status
        }
    }), 201


@bp.route('/<uuid:listing_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_listing(listing_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    listing, error = marketplace_listing_service.get_by_id_for_user(
        listing_id=listing_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace listing not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You do not have permission to view this listing'
        }), 403

    return jsonify({
        'id': str(listing.id),
        'seller_id': str(listing.seller_id),
        'category': listing.category,
        'title': listing.title,
        'description': listing.description,
        'price': listing.price,
        'quantity': listing.quantity,
        'status': listing.status,
        'created_at': listing.created_at,
        'updated_at': listing.updated_at
    }), 200


@bp.route('/<uuid:listing_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def update_listing(listing_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    listing, error = marketplace_listing_service.update(
        listing_id=listing_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace listing not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only update your own listings'
        }), 403

    return jsonify({
        'message': 'Marketplace listing updated successfully',
        'listing': {
            'id': str(listing.id),
            'seller_id': str(listing.seller_id),
            'category': listing.category,
            'title': listing.title,
            'description': listing.description,
            'price': listing.price,
            'quantity': listing.quantity,
            'status': listing.status
        }
    }), 200


@bp.route('/<uuid:listing_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def delete_listing(listing_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = marketplace_listing_service.delete(
        listing_id=listing_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Marketplace listing not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only delete your own listings'
        }), 403

    return jsonify({
        'message': 'Marketplace listing deleted successfully'
    }), 200