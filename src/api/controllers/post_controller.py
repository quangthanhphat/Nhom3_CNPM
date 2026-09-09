from flask import (
    Blueprint,
    jsonify,
    request,
    send_from_directory
)

from services.post_service import PostService
from services.storage_service import STORAGE_DIR
from infrastructure.models.generated_models import PostImages
from api.middleware import token_required, role_required


bp = Blueprint(
    'post',
    __name__,
    url_prefix='/posts'
)

post_service = PostService()


# =========================
# GET POST IMAGES
# =========================

def get_post_images(post_id):

    images = (
        post_service.repository.session
        .query(PostImages)
        .filter(PostImages.post_id == post_id)
        .all()
    )

    return [
        {
            'id': str(image.id),
            'image_path': image.image_path
        }
        for image in images
    ]


# =========================
# GET ALL POSTS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
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

        images = get_post_images(post.id)

        result.append({
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'images': images
        })

    return jsonify(result), 200


# =========================
# CREATE POST
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'photography_expert'
)
def create_post():

    data = {
        'type': request.form.get('type'),
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'status': request.form.get(
            'status',
            'published'
        )
    }

    if not data.get('type'):
        return jsonify({
            'message': 'Post type is required'
        }), 400

    if not data.get('title'):
        return jsonify({
            'message': 'Post title is required'
        }), 400

    if not data.get('content'):
        return jsonify({
            'message': 'Post content is required'
        }), 400

    # Flutter upload ảnh bằng field name "images"
    image_files = request.files.getlist('images')

    author_id = request.user.get('user_id')

    post = post_service.create(
        author_id=author_id,
        data=data,
        image_files=image_files
    )

    images = get_post_images(post.id)

    return jsonify({
        'message': 'Post created successfully',
        'post': {
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'images': images
        }
    }), 201


# =========================
# GET POST BY ID
# =========================

@bp.route('/<uuid:post_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
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

    images = get_post_images(post.id)

    return jsonify({
        'id': str(post.id),
        'author_id': str(post.author_id),
        'type': post.type,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
        'images': images
    }), 200


# =========================
# UPDATE POST
# =========================

@bp.route('/<uuid:post_id>', methods=['PUT'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def update_post(post_id):

    data = {
        'type': request.form.get('type'),
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'status': request.form.get('status')
    }

    data = {
        key: value
        for key, value in data.items()
        if value is not None
    }

    image_files = request.files.getlist('images')

    if not data and not image_files:
        return jsonify({
            'message': 'No data to update'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    post, error = post_service.update(
        post_id=post_id,
        data=data,
        user_id=user_id,
        role=role,
        image_files=image_files
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

    images = get_post_images(post.id)

    return jsonify({
        'message': 'Post updated successfully',
        'post': {
            'id': str(post.id),
            'author_id': str(post.author_id),
            'type': post.type,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'images': images
        }
    }), 200


# =========================
# DELETE POST
# =========================

@bp.route('/<uuid:post_id>', methods=['DELETE'])
@token_required
@role_required(
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


# =========================
# SERVE POST IMAGES
# =========================

@bp.route(
    '/images/<path:storage_path>',
    methods=['GET']
)
def serve_post_image(storage_path):

    storage_path = storage_path.replace(
        '\\',
        '/'
    )

    file_path = STORAGE_DIR / storage_path

    if (
        not file_path.exists()
        or not file_path.is_file()
    ):
        return jsonify({
            'message': 'Image not found'
        }), 404

    return send_from_directory(
        str(file_path.parent),
        file_path.name
    )