from flask import Blueprint, jsonify, request

from services.digital_scan_service import DigitalScanService
from api.middleware import token_required, role_required


bp = Blueprint(
    'digital_scan_api',
    __name__,
    url_prefix='/digital-scans'
)

digital_scan_service = DigitalScanService()


# =========================
# GET ALL SCANS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_all_scans():
    scans = digital_scan_service.list_for_user(
        user_id=request.user.get('user_id'),
        role=request.user.get('role')
    )

    result = []

    for scan in scans:
        result.append({
            'id': str(scan.id),
            'order_id': str(scan.order_id),
            'customer_id': str(scan.customer_id),
            'file_name': scan.file_name,
            'storage_path': scan.storage_path,
            'file_size': scan.file_size,
            'scan_specification': scan.scan_specification,
            'scan_quality': scan.scan_quality,
            'film_stock': scan.film_stock,
            'camera_model': scan.camera_model,
            'lens': scan.lens,
            'shooting_date': scan.shooting_date,
            'processing_method': scan.processing_method,
            'uploaded_at': scan.uploaded_at
        })

    return jsonify(result), 200


# =========================
# CREATE SCAN
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'customer'
)
def create_scan():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('order_id'):
        return jsonify({
            'message': 'order_id is required'
        }), 400

    if not data.get('file_name'):
        return jsonify({
            'message': 'file_name is required'
        }), 400

    if not data.get('storage_path'):
        return jsonify({
            'message': 'storage_path is required'
        }), 400

    customer_id = request.user.get('user_id')

    scan = digital_scan_service.create(
        customer_id=customer_id,
        data=data
    )

    return jsonify({
        'message': 'Digital scan created successfully',
        'scan': {
            'id': str(scan.id),
            'order_id': str(scan.order_id),
            'customer_id': str(scan.customer_id),
            'file_name': scan.file_name,
            'storage_path': scan.storage_path,
            'file_size': scan.file_size,
            'scan_specification': scan.scan_specification,
            'scan_quality': scan.scan_quality,
            'film_stock': scan.film_stock,
            'camera_model': scan.camera_model,
            'lens': scan.lens,
            'shooting_date': scan.shooting_date,
            'processing_method': scan.processing_method,
            'uploaded_at': scan.uploaded_at
        }
    }), 201


# =========================
# GET SCAN BY ID
# =========================

@bp.route('/<uuid:scan_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'admin'
)
def get_scan(scan_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    scan, error = digital_scan_service.get_by_id_for_user(
        scan_id=scan_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital scan not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this digital scan'
            )
        }), 403

    return jsonify({
        'id': str(scan.id),
        'order_id': str(scan.order_id),
        'customer_id': str(scan.customer_id),
        'file_name': scan.file_name,
        'storage_path': scan.storage_path,
        'file_size': scan.file_size,
        'scan_specification': scan.scan_specification,
        'scan_quality': scan.scan_quality,
        'film_stock': scan.film_stock,
        'camera_model': scan.camera_model,
        'lens': scan.lens,
        'shooting_date': scan.shooting_date,
        'processing_method': scan.processing_method,
        'uploaded_at': scan.uploaded_at
    }), 200


# =========================
# UPDATE SCAN
# =========================

@bp.route('/<uuid:scan_id>', methods=['PUT'])
@token_required
@role_required(
    'customer',
    'admin'
)
def update_scan(scan_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    scan, error = digital_scan_service.update(
        scan_id=scan_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital scan not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to update this digital scan'
            )
        }), 403

    return jsonify({
        'message': 'Digital scan updated successfully',
        'scan': {
            'id': str(scan.id),
            'order_id': str(scan.order_id),
            'customer_id': str(scan.customer_id),
            'file_name': scan.file_name,
            'storage_path': scan.storage_path,
            'file_size': scan.file_size,
            'scan_specification': scan.scan_specification,
            'scan_quality': scan.scan_quality,
            'film_stock': scan.film_stock,
            'camera_model': scan.camera_model,
            'lens': scan.lens,
            'shooting_date': scan.shooting_date,
            'processing_method': scan.processing_method,
            'uploaded_at': scan.uploaded_at
        }
    }), 200


# =========================
# DELETE SCAN
# =========================

@bp.route('/<uuid:scan_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'admin'
)
def delete_scan(scan_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = digital_scan_service.delete(
        scan_id=scan_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Digital scan not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this digital scan'
            )
        }), 403

    return jsonify({
        'message': 'Digital scan deleted successfully'
    }), 200