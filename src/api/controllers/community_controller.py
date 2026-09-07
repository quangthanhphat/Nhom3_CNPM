from flask import Blueprint, jsonify, request

from api.middleware import token_required
from services.community_service import CommunityService

bp = Blueprint('community', __name__, url_prefix='/community')
community_service = None


def _service():
    global community_service
    if community_service is None:
        community_service = CommunityService()
    return community_service


def _user_id():
    return request.user.get('user_id')


def _post(post):
    return {'id': str(post.id), 'author_id': str(post.author_id), 'type': post.type,
            'title': post.title, 'content': post.content, 'status': post.status,
            'created_at': post.created_at.isoformat() if post.created_at else None,
            'updated_at': post.updated_at.isoformat() if post.updated_at else None}


def _comment(comment):
    return {'id': str(comment.id), 'post_id': str(comment.post_id),
            'author_id': str(comment.author_id), 'content': comment.content,
            'created_at': comment.created_at.isoformat() if comment.created_at else None,
            'updated_at': comment.updated_at.isoformat() if comment.updated_at else None}


def _error(error, status=400):
    return jsonify({'message': str(error)}), status


@bp.route('/posts', methods=['GET'])
def list_posts():
    return jsonify([_post(post) for post in _service().list_posts(request.args.get('status'))]), 200


@bp.route('/posts/<uuid:post_id>', methods=['GET'])
def get_post(post_id):
    post = _service().get_post(post_id)
    return (jsonify(_post(post)), 200) if post else _error('Post not found', 404)


@bp.route('/posts', methods=['POST'])
@token_required
def create_post():
    try:
        return jsonify(_post(_service().create_post(_user_id(), request.get_json(silent=True) or {}))), 201
    except (ValueError, PermissionError) as error:
        return _error(error, 400)


@bp.route('/posts/<uuid:post_id>', methods=['PATCH'])
@token_required
def update_post(post_id):
    try:
        post = _service().update_post(post_id, _user_id(), request.get_json(silent=True) or {})
        return (jsonify(_post(post)), 200) if post else _error('Post not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error, 400)


@bp.route('/posts/<uuid:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    try:
        deleted = _service().delete_post(post_id, _user_id())
        return (jsonify({'message': 'Post deleted'}), 200) if deleted else _error('Post not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error, 400)


@bp.route('/posts/<uuid:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    comments = _service().list_comments(post_id)
    return (jsonify([_comment(comment) for comment in comments]), 200) if comments is not None else _error('Post not found', 404)


@bp.route('/posts/<uuid:post_id>/comments', methods=['POST'])
@token_required
def create_comment(post_id):
    try:
        comment = _service().create_comment(post_id, _user_id(), request.get_json(silent=True) or {})
        return (jsonify(_comment(comment)), 201) if comment else _error('Post not found', 404)
    except ValueError as error: return _error(error, 400)


@bp.route('/comments/<uuid:comment_id>', methods=['PATCH'])
@token_required
def update_comment(comment_id):
    try:
        comment = _service().update_comment(comment_id, _user_id(), request.get_json(silent=True) or {})
        return (jsonify(_comment(comment)), 200) if comment else _error('Comment not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error, 400)


@bp.route('/comments/<uuid:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    try:
        deleted = _service().delete_comment(comment_id, _user_id())
        return (jsonify({'message': 'Comment deleted'}), 200) if deleted else _error('Comment not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error, 400)
