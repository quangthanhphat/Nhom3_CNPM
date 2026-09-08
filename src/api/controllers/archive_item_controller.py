from flask import Blueprint, jsonify, request

from services.archive_item_service import ArchiveItemService
from api.middleware import token_required, role_required


bp = Blueprint(
    'archive_item',
    __name__,
    url_prefix='/archive-items'
)

archive_item_service = ArchiveItemService()


# =========================
# GET ALL ARCHIVE ITEMS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_all_archive_items():
    items = archive_item_service.list_for_user(
        user_id=request.user.get('user_id'),
        role=request.user.get('role')
    )

    result = []

    for item in items:
        result.append({
            'id': str(item.id),
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),
            'added_at': item.added_at
        })

    return jsonify(result), 200


# =========================
# CREATE ARCHIVE ITEM
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer',
    'admin'
)
def create_archive_item():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('archive_id'):
        return jsonify({
            'message': 'archive_id is required'
        }), 400

    if not data.get('scan_id'):
        return jsonify({
            'message': 'scan_id is required'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    item, error = archive_item_service.create(
        data=data,
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
                'You can only add your own scan '
                'to your own archive'
            )
        }), 403

    return jsonify({
        'message': 'Archive item created successfully',
        'archive_item': {
            'id': str(item.id),
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),
            'added_at': item.added_at
        }
    }), 201


# =========================
# GET ARCHIVE ITEM BY ID
# =========================

@bp.route('/<uuid:archive_item_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_archive_item(archive_item_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    item, error = archive_item_service.get_by_id_for_user(
        archive_item_id=archive_item_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Archive item not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this archive item'
            )
        }), 403

    return jsonify({
        'id': str(item.id),
        'archive_id': str(item.archive_id),
        'scan_id': str(item.scan_id),
        'added_at': item.added_at
    }), 200


# =========================
# UPDATE ARCHIVE ITEM
# =========================

@bp.route('/<uuid:archive_item_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'admin'
)
def update_archive_item(archive_item_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    item, error = archive_item_service.update(
        archive_item_id=archive_item_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Archive item not found'
        }), 404

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
                'to update this archive item'
            )
        }), 403

    return jsonify({
        'message': 'Archive item updated successfully',
        'archive_item': {
            'id': str(item.id),
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),
            'added_at': item.added_at
        }
    }), 200


# =========================
# DELETE ARCHIVE ITEM
# =========================

@bp.route('/<uuid:archive_item_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'admin'
)
def delete_archive_item(archive_item_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = archive_item_service.delete(
        archive_item_id=archive_item_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Archive item not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this archive item'
            )
        }), 403

    return jsonify({
        'message': 'Archive item deleted successfully'
    }), 200