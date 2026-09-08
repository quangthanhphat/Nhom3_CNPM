from flask import Blueprint, jsonify, request

from services.digital_film_archive_service import DigitalFilmArchiveService
from api.middleware import token_required, role_required


bp = Blueprint(
    'digital_film_archive',
    __name__,
    url_prefix='/digital-film-archives'
)

digital_film_archive_service = DigitalFilmArchiveService()


# =========================
# GET ALL ARCHIVES
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_all_archives():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    archives = digital_film_archive_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for archive in archives:
        result.append({
            'id': str(archive.id),
            'customer_id': str(archive.customer_id),
            'name': archive.name,
            'description': archive.description
        })

    return jsonify(result), 200


# =========================
# CREATE ARCHIVE
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer'
)
def create_archive():
    data = request.get_json()

    customer_id = request.user.get('user_id')

    archive = digital_film_archive_service.create(
        customer_id=customer_id,
        data=data
    )

    return jsonify({
        'message': 'Digital film archive created successfully',
        'archive': {
            'id': str(archive.id),
            'customer_id': str(archive.customer_id),
            'name': archive.name,
            'description': archive.description
        }
    }), 201


# =========================
# GET ARCHIVE BY ID
# =========================

@bp.route('/<uuid:archive_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_archive(archive_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    archive, error = digital_film_archive_service.get_by_id_for_user(
        archive_id=archive_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital film archive not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this archive'
            )
        }), 403

    return jsonify({
        'id': str(archive.id),
        'customer_id': str(archive.customer_id),
        'name': archive.name,
        'description': archive.description
    }), 200


# =========================
# UPDATE ARCHIVE
# =========================

@bp.route('/<uuid:archive_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'admin'
)
def update_archive(archive_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    archive, error = digital_film_archive_service.update(
        archive_id=archive_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital film archive not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to update this archive'
            )
        }), 403

    return jsonify({
        'message': 'Digital film archive updated successfully',
        'archive': {
            'id': str(archive.id),
            'customer_id': str(archive.customer_id),
            'name': archive.name,
            'description': archive.description
        }
    }), 200


# =========================
# DELETE ARCHIVE
# =========================

@bp.route('/<uuid:archive_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'admin'
)
def delete_archive(archive_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = digital_film_archive_service.delete(
        archive_id=archive_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital film archive not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this archive'
            )
        }), 403

    return jsonify({
        'message': 'Digital film archive deleted successfully'
    }), 200