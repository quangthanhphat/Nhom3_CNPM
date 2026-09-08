from flask import Blueprint, jsonify, request

from services.comment_service import CommentService
from api.middleware import token_required, role_required


bp = Blueprint(
    'comment',
    __name__,
    url_prefix='/comments'
)

comment_service = CommentService()


# =========================
# GET ALL COMMENTS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_all_comments():
    comments = comment_service.list_for_user(
        user_id=request.user.get('user_id'),
        role=request.user.get('role')
    )

    result = []

    for comment in comments:
        result.append({
            'id': str(comment.id),
            'post_id': str(comment.post_id),
            'author_id': str(comment.author_id),
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        })

    return jsonify(result), 200


# =========================
# CREATE COMMENT
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'photography_expert'
)
def create_comment():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('post_id'):
        return jsonify({
            'message': 'post_id is required'
        }), 400

    if not data.get('content'):
        return jsonify({
            'message': 'content is required'
        }), 400

    author_id = request.user.get('user_id')

    comment = comment_service.create(
        author_id=author_id,
        data=data
    )

    return jsonify({
        'message': 'Comment created successfully',
        'comment': {
            'id': str(comment.id),
            'post_id': str(comment.post_id),
            'author_id': str(comment.author_id),
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        }
    }), 201


# =========================
# GET COMMENT BY ID
# =========================

@bp.route('/<uuid:comment_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_comment(comment_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    comment, error = comment_service.get_by_id_for_user(
        comment_id=comment_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Comment not found'
        }), 404

    return jsonify({
        'id': str(comment.id),
        'post_id': str(comment.post_id),
        'author_id': str(comment.author_id),
        'content': comment.content,
        'created_at': comment.created_at,
        'updated_at': comment.updated_at
    }), 200


# =========================
# UPDATE COMMENT
# =========================

@bp.route('/<uuid:comment_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def update_comment(comment_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    comment, error = comment_service.update(
        comment_id=comment_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Comment not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only update '
                'your own comments'
            )
        }), 403

    return jsonify({
        'message': 'Comment updated successfully',
        'comment': {
            'id': str(comment.id),
            'post_id': str(comment.post_id),
            'author_id': str(comment.author_id),
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        }
    }), 200


# =========================
# DELETE COMMENT
# =========================

@bp.route('/<uuid:comment_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def delete_comment(comment_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = comment_service.delete(
        comment_id=comment_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Comment not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only delete '
                'your own comments'
            )
        }), 403

    return jsonify({
        'message': 'Comment deleted successfully'
    }), 200