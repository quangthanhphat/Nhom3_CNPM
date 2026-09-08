from flask import Blueprint, jsonify, request

from services.favorite_service import FavoriteService
from api.middleware import token_required, role_required


bp = Blueprint(
    'favorite',
    __name__,
    url_prefix='/favorites'
)

favorite_service = FavoriteService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_all_favorites():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    favorites = favorite_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for favorite in favorites:
        result.append({
            'id': str(favorite.id),
            'user_id': str(favorite.user_id),
            'target_type': favorite.target_type,
            'target_id': str(favorite.target_id),
            'created_at': favorite.created_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert'
)
def create_favorite():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('target_type'):
        return jsonify({
            'message': 'target_type is required'
        }), 400

    if not data.get('target_id'):
        return jsonify({
            'message': 'target_id is required'
        }), 400

    user_id = request.user.get('user_id')

    favorite = favorite_service.create(
        user_id=user_id,
        data=data
    )

    return jsonify({
        'message': 'Favorite created successfully',
        'favorite': {
            'id': str(favorite.id),
            'user_id': str(favorite.user_id),
            'target_type': favorite.target_type,
            'target_id': str(favorite.target_id),
            'created_at': favorite.created_at
        }
    }), 201


@bp.route('/<uuid:favorite_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_favorite(favorite_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    favorite, error = favorite_service.get_by_id_for_user(
        favorite_id=favorite_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Favorite not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You do not have permission to view this favorite'
        }), 403

    return jsonify({
        'id': str(favorite.id),
        'user_id': str(favorite.user_id),
        'target_type': favorite.target_type,
        'target_id': str(favorite.target_id),
        'created_at': favorite.created_at
    }), 200


@bp.route('/<uuid:favorite_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def delete_favorite(favorite_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = favorite_service.delete(
        favorite_id=favorite_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Favorite not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only delete your own favorites'
        }), 403

    return jsonify({
        'message': 'Favorite deleted successfully'
    }), 200