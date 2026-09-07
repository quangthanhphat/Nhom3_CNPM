from flask import Blueprint, jsonify, request

from api.middleware import token_required
from services.digital_film_service import DigitalFilmService


bp = Blueprint('digital_film', __name__, url_prefix='/digital-film')
digital_film_service = DigitalFilmService()


def archive_response(archive):
    return {
        'id': str(archive.id),
        'customer_id': str(archive.customer_id),
        'name': archive.name,
        'description': archive.description,
        'created_at': archive.created_at.isoformat() if archive.created_at else None,
        'updated_at': archive.updated_at.isoformat() if archive.updated_at else None,
        'scan_ids': [str(item.scan_id) for item in archive.archive_items]
    }


def scan_response(scan):
    return {
        'id': str(scan.id),
        'order_id': str(scan.order_id),
        'customer_id': str(scan.customer_id),
        'file_name': scan.file_name,
        'storage_path': scan.storage_path,
        'uploaded_at': scan.uploaded_at.isoformat() if scan.uploaded_at else None,
        'file_size': scan.file_size,
        'scan_specification': scan.scan_specification,
        'scan_quality': scan.scan_quality,
        'film_stock': scan.film_stock,
        'camera_model': scan.camera_model,
        'lens': scan.lens,
        'shooting_date': scan.shooting_date.isoformat() if scan.shooting_date else None,
        'processing_method': scan.processing_method
    }


def current_customer_id():
    return request.user.get('user_id')


@bp.route('/archives', methods=['GET'])
@token_required
def list_archives():
    archives = digital_film_service.list_archives(current_customer_id())
    return jsonify([archive_response(archive) for archive in archives]), 200


@bp.route('/archives', methods=['POST'])
@token_required
def create_archive():
    archive = digital_film_service.create_archive(
        current_customer_id(), request.get_json(silent=True) or {}
    )
    if not archive:
        return jsonify({'message': 'name is required'}), 400
    return jsonify(archive_response(archive)), 201


@bp.route('/archives/<uuid:archive_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def archive_detail(archive_id):
    customer_id = current_customer_id()
    if request.method == 'GET':
        archive = digital_film_service.get_archive(archive_id, customer_id)
        if not archive:
            return jsonify({'message': 'Archive not found'}), 404
        return jsonify(archive_response(archive)), 200

    if request.method == 'PUT':
        archive = digital_film_service.update_archive(
            archive_id, customer_id, request.get_json(silent=True) or {}
        )
        if not archive:
            return jsonify({'message': 'Archive not found'}), 404
        return jsonify(archive_response(archive)), 200

    if not digital_film_service.delete_archive(archive_id, customer_id):
        return jsonify({'message': 'Archive not found'}), 404
    return jsonify({'message': 'Archive deleted successfully'}), 200


@bp.route('/scans', methods=['GET'])
@token_required
def list_scans():
    scans = digital_film_service.list_scans(current_customer_id())
    return jsonify([scan_response(scan) for scan in scans]), 200


@bp.route('/scans', methods=['POST'])
@token_required
def create_scan():
    scan = digital_film_service.create_scan(
        current_customer_id(), request.get_json(silent=True) or {}
    )
    if not scan:
        return jsonify({
            'message': 'order_id, file_name and storage_path are required'
        }), 400
    return jsonify(scan_response(scan)), 201


@bp.route('/scans/<uuid:scan_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def scan_detail(scan_id):
    customer_id = current_customer_id()
    if request.method == 'GET':
        scan = digital_film_service.get_scan(scan_id, customer_id)
        if not scan:
            return jsonify({'message': 'Scan not found'}), 404
        return jsonify(scan_response(scan)), 200

    if request.method == 'PUT':
        scan = digital_film_service.update_scan(
            scan_id, customer_id, request.get_json(silent=True) or {}
        )
        if not scan:
            return jsonify({'message': 'Scan not found'}), 404
        return jsonify(scan_response(scan)), 200

    if not digital_film_service.delete_scan(scan_id, customer_id):
        return jsonify({'message': 'Scan not found'}), 404
    return jsonify({'message': 'Scan deleted successfully'}), 200


@bp.route('/archives/<uuid:archive_id>/scans/<uuid:scan_id>', methods=['POST', 'DELETE'])
@token_required
def archive_scan(archive_id, scan_id):
    customer_id = current_customer_id()
    if request.method == 'POST':
        item = digital_film_service.add_scan_to_archive(
            archive_id, scan_id, customer_id
        )
        if not item:
            return jsonify({'message': 'Archive or scan not found'}), 404
        return jsonify({
            'archive_id': str(item.archive_id),
            'scan_id': str(item.scan_id),
            'added_at': item.added_at.isoformat() if item.added_at else None
        }), 201

    if not digital_film_service.remove_scan_from_archive(
        archive_id, scan_id, customer_id
    ):
        return jsonify({'message': 'Archive item not found'}), 404
    return jsonify({'message': 'Scan removed from archive'}), 200
