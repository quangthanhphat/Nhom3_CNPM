from flask import Blueprint, jsonify, request

from services.rating_service import RatingService
from api.middleware import token_required, role_required


bp = Blueprint(
    'rating',
    __name__,
    url_prefix='/ratings'
)

rating_service = RatingService()


def rating_to_dict(rating):
    return {
        'id': str(rating.id),
        'user_id': str(rating.user_id),
        'target_type': rating.target_type,
        'target_id': str(rating.target_id),
        'rating': rating.rating,
        'review': rating.review,
        'created_at': rating.created_at
    }


# =========================
# GET ALL RATINGS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_all_ratings():

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    ratings = rating_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = [
        rating_to_dict(rating)
        for rating in ratings
    ]

    return jsonify(result), 200


# =========================
# GET RATINGS FOR POST
# =========================

@bp.route('/post/<uuid:post_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def get_post_ratings(post_id):

    user_id = request.user.get('user_id')

    ratings = rating_service.list_for_post(
        post_id=post_id
    )

    # =========================
    # CALCULATE PUBLIC SUMMARY
    # =========================

    count = len(ratings)

    if count > 0:
        average = sum(
            rating.rating
            for rating in ratings
        ) / count
    else:
        average = 0

    # =========================
    # GET CURRENT USER RATING
    # =========================

    my_rating = rating_service.get_user_rating_for_post(
        post_id=post_id,
        user_id=user_id
    )

    return jsonify({
        'ratings': [
            rating_to_dict(rating)
            for rating in ratings
        ],
        'average': round(average, 1),
        'count': count,
        'my_rating': (
            rating_to_dict(my_rating)
            if my_rating
            else None
        )
    }), 200


# =========================
# CREATE RATING
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert'
)
def create_rating():

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if data.get('target_type') != 'post':
        return jsonify({
            'message': 'target_type must be post'
        }), 400

    if not data.get('target_id'):
        return jsonify({
            'message': 'target_id is required'
        }), 400

    if data.get('rating') is None:
        return jsonify({
            'message': 'rating is required'
        }), 400

    if (
        not isinstance(data.get('rating'), int)
        or not 1 <= data.get('rating') <= 5
    ):
        return jsonify({
            'message': 'rating must be between 1 and 5'
        }), 400

    user_id = request.user.get('user_id')

    rating = rating_service.create(
        user_id=user_id,
        data=data
    )

    return jsonify({
        'message': 'Rating saved successfully',
        'rating': rating_to_dict(rating)
    }), 200


# =========================
# GET RATING BY ID
# =========================

@bp.route('/<uuid:rating_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
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

    return jsonify(
        rating_to_dict(rating)
    ), 200


# =========================
# UPDATE RATING
# =========================

@bp.route('/<uuid:rating_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'admin'
)
def update_rating(rating_id):

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if 'rating' in data:
        if (
            not isinstance(data.get('rating'), int)
            or not 1 <= data.get('rating') <= 5
        ):
            return jsonify({
                'message': 'rating must be between 1 and 5'
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
        'rating': rating_to_dict(rating)
    }), 200


# =========================
# DELETE RATING
# =========================

@bp.route('/<uuid:rating_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
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