from flask import Blueprint, jsonify, request

from services.comment_service import CommentService
from infrastructure.repositories.comment_repository import CommentRepository
from infrastructure.models.generated_models import Users
from api.middleware import token_required, role_required


bp = Blueprint(
    'comment',
    __name__,
    url_prefix='/comments'
)

comment_service = CommentService()
comment_repository = CommentRepository()


# =========================================================
# HELPER
# =========================================================

def unpack_comment_item(item):
    """
    Repository có thể trả về:
    - (Comments, Users)
    - SQLAlchemy Row(Comments, Users)
    - Comments
    """

    if isinstance(item, tuple):
        if len(item) >= 2:
            return item[0], item[1]

        if len(item) == 1:
            return item[0], None

    # SQLAlchemy Row
    try:
        if hasattr(item, '_mapping'):
            mapping = item._mapping

            comment = mapping.get('Comments')
            user = mapping.get('Users')

            if comment is not None:
                return comment, user
    except Exception:
        pass

    # Trường hợp chỉ trả về Comments
    return item, None


def serialize_comment(comment, user=None):

    # Nếu repository chưa trả User thì tìm User
    # dựa trên author_id của comment.
    if user is None:
        user = (
            comment_repository.session
            .query(Users)
            .filter(Users.id == comment.author_id)
            .first()
        )

    return {
        'id': str(comment.id),
        'post_id': str(comment.post_id),
        'author_id': str(comment.author_id),

        'author_name': (
            user.full_name
            if user and user.full_name
            else None
        ),

        'author_username': (
            user.username
            if user and user.username
            else None
        ),

        'author_avatar_url': (
            user.avatar_url
            if user and user.avatar_url
            else None
        ),

        'content': comment.content,

        'created_at': (
            comment.created_at.isoformat()
            if comment.created_at
            else None
        ),

        'updated_at': (
            comment.updated_at.isoformat()
            if comment.updated_at
            else None
        )
    }


# =========================================================
# GET ALL COMMENTS
# =========================================================

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

    for item in comments:

        comment, user = unpack_comment_item(item)

        if not comment:
            continue

        result.append(
            serialize_comment(
                comment,
                user
            )
        )

    return jsonify(result), 200


# =========================================================
# GET COMMENTS BY POST
# =========================================================

@bp.route('/post/<uuid:post_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_comments_by_post(post_id):

    # Lấy trực tiếp comment của post này
    comments = comment_repository.list_for_post(post_id)

    result = []

    for item in comments:

        comment, user = unpack_comment_item(item)

        if not comment:
            continue

        result.append(
            serialize_comment(
                comment,
                user
            )
        )

    return jsonify(result), 200


# =========================================================
# CREATE COMMENT
# =========================================================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
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
        'comment': serialize_comment(comment)
    }), 201


# =========================================================
# GET COMMENT BY ID
# =========================================================

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

    return jsonify(
        serialize_comment(comment)
    ), 200


# =========================================================
# UPDATE COMMENT
# =========================================================

@bp.route('/<uuid:comment_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
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
        'comment': serialize_comment(comment)
    }), 200


# =========================================================
# DELETE COMMENT
# =========================================================

@bp.route('/<uuid:comment_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
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