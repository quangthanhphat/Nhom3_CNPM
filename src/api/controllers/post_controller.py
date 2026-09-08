from flask import Blueprint, jsonify, request

from services.post_service import PostService
from api.middleware import token_required, role_required


bp = Blueprint(
    'post',
    __name__,
    url_prefix='/posts'
)

post_service = PostService()


# =========================
# GET ALL POSTS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def get_all_posts():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    posts = post_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for post in posts:
        result.append({
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'created_at': post.created_at,
            'updated_at': post.updated_at
        })

    return jsonify(result), 200


# =========================
# CREATE POST
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'photography_expert'
)
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    author_id = request.user.get('user_id')

    post = post_service.create(
        author_id=author_id,
        data=data
    )

    return jsonify({
        'message': 'Post created successfully',
        'post': {
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status
        }
    }), 201


# =========================
# GET POST BY ID
# =========================

@bp.route('/<uuid:post_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def get_post(post_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    post, error = post_service.get_by_id_for_user(
        post_id=post_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Post not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this post'
            )
        }), 403

    return jsonify({
        'id': str(post.id),
        'author_id': str(post.author_id),
        'type': post.type,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'created_at': post.created_at,
        'updated_at': post.updated_at
    }), 200


# =========================
# UPDATE POST
# =========================

@bp.route('/<uuid:post_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def update_post(post_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    post, error = post_service.update(
        post_id=post_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Post not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only update '
                'your own posts'
            )
        }), 403

    return jsonify({
        'message': 'Post updated successfully',
        'post': {
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status
        }
    }), 200


# =========================
# DELETE POST
# =========================

@bp.route('/<uuid:post_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def delete_post(post_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = post_service.delete(
        post_id=post_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Post not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only delete '
                'your own posts'
            )
        }), 403

    return jsonify({
        'message': 'Post deleted successfully'
    }), 200