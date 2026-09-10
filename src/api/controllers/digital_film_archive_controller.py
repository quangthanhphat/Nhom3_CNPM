from flask import Blueprint, jsonify, request

from services.digital_film_archive_service import DigitalFilmArchiveService
from services.archive_item_service import ArchiveItemService
from api.middleware import token_required, role_required


bp = Blueprint(
    'digital_film_archive',
    __name__,
    url_prefix='/digital-film-archives'
)

digital_film_archive_service = DigitalFilmArchiveService()
archive_item_service = ArchiveItemService()


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
    data = request.get_json() or {}

    if not data.get('name'):
        return jsonify({
            'message': 'Archive name is required'
        }), 400

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
# GET FILES IN ARCHIVE
# =========================

@bp.route('/<uuid:archive_id>/items', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_archive_items(archive_id):
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

    items = archive_item_service.repository.list_by_archive_id(
        archive_id
    )

    result = []

    for item, scan in items:
        result.append({
            'id': str(item.id),
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),

            # Quan trọng:
            # Dùng order_id + scan_id để Flutter
            # lấy file ảnh thật từ Order Result.
            'order_id': str(scan.order_id),

            'file_name': scan.file_name,
            'storage_path': scan.storage_path,
            'file_size': scan.file_size,
            'uploaded_at': (
                scan.uploaded_at.isoformat()
                if scan.uploaded_at
                else None
            ),
            'added_at': (
                item.added_at.isoformat()
                if item.added_at
                else None
            )
        })

    return jsonify({
        'archive': {
            'id': str(archive.id),
            'name': archive.name,
            'description': archive.description
        },
        'items': result
    }), 200


# =========================
# ADD SCAN TO ARCHIVE
# =========================

@bp.route(
    '/<uuid:archive_id>/items',
    methods=['POST']
)
@token_required
@role_required(
    'customer',
    'admin'
)
def add_scan_to_archive(archive_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    data = request.get_json() or {}

    scan_id = data.get('scan_id')

    if not scan_id:
        return jsonify({
            'message': 'scan_id is required'
        }), 400

    item, error = archive_item_service.create(
        data={
            'archive_id': str(archive_id),
            'scan_id': scan_id
        },
        user_id=user_id,
        role=role
    )

    if error == 'archive_not_found':
        return jsonify({
            'message': 'Digital film archive not found'
        }), 404

    if error == 'scan_not_found':
        return jsonify({
            'message': 'Digital scan not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to add this scan to the archive'
            )
        }), 403

    return jsonify({
        'message': 'Scan added to archive successfully',
        'item': {
            'id': str(item.id),
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),
            'added_at': (
                item.added_at.isoformat()
                if item.added_at
                else None
            )
        }
    }), 201


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
    data = request.get_json() or {}

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