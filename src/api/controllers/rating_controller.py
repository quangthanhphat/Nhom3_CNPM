from flask import Blueprint, jsonify, request

from services.rating_service import RatingService
from api.middleware import token_required, role_required


bp = Blueprint(
    'rating',
    __name__,
    url_prefix='/ratings'
)

rating_service = RatingService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_all_ratings():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    ratings = rating_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for rating in ratings:
        result.append({
            'id': str(rating.id),
            'user_id': str(rating.user_id),
            'order_id': str(rating.order_id),
            'rating': rating.rating,
            'review_text': rating.review_text,
            'created_at': rating.created_at,
            'updated_at': rating.updated_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required('customer')
def create_rating():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('order_id'):
        return jsonify({
            'message': 'order_id is required'
        }), 400

    if data.get('rating') is None:
        return jsonify({
            'message': 'rating is required'
        }), 400

    if not isinstance(data.get('rating'), int) or not 1 <= data.get('rating') <= 5:
        return jsonify({
            'message': 'rating must be between 1 and 5'
        }), 400

    user_id = request.user.get('user_id')

    rating = rating_service.create(
        user_id=user_id,
        data=data
    )

    return jsonify({
        'message': 'Rating created successfully',
        'rating': {
            'id': str(rating.id),
            'user_id': str(rating.user_id),
            'order_id': str(rating.order_id),
            'rating': rating.rating,
            'review_text': rating.review_text
        }
    }), 201


@bp.route('/<uuid:rating_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_rating(rating_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    rating, error = rating_service.get_by_id_for_user(
        rating_id=rating_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Rating not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this rating'
            )
        }), 403

    return jsonify({
        'id': str(rating.id),
        'user_id': str(rating.user_id),
        'order_id': str(rating.order_id),
        'rating': rating.rating,
        'review_text': rating.review_text,
        'created_at': rating.created_at,
        'updated_at': rating.updated_at
    }), 200


@bp.route('/<uuid:rating_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'admin'
)
def update_rating(rating_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    rating, error = rating_service.update(
        rating_id=rating_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Rating not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only update your own ratings'
        }), 403

    return jsonify({
        'message': 'Rating updated successfully',
        'rating': {
            'id': str(rating.id),
            'user_id': str(rating.user_id),
            'order_id': str(rating.order_id),
            'rating': rating.rating,
            'review_text': rating.review_text
        }
    }), 200


@bp.route('/<uuid:rating_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'admin'
)
def delete_rating(rating_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = rating_service.delete(
        rating_id=rating_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Rating not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only delete your own ratings'
        }), 403

    return jsonify({
        'message': 'Rating deleted successfully'
    }), 200