from flask import Blueprint, jsonify, request

from services.photowalk_service import PhotowalkService
from api.middleware import token_required, role_required


bp = Blueprint(
    'photowalk',
    __name__,
    url_prefix='/photowalks'
)

photowalk_service = PhotowalkService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_all_photowalks():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    photowalks = photowalk_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for photowalk in photowalks:
        result.append({
            'id': str(photowalk.id),
            'organizer_id': str(photowalk.organizer_id),
            'title': photowalk.title,
            'description': photowalk.description,
            'location': photowalk.location,
            'start_time': photowalk.start_time,
            'end_time': photowalk.end_time,
            'capacity': photowalk.capacity,
            'status': photowalk.status
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def create_photowalk():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    organizer_id = request.user.get('user_id')

    photowalk = photowalk_service.create(
        organizer_id=organizer_id,
        data=data
    )

    return jsonify({
        'message': 'Photowalk created successfully',
        'photowalk': {
            'id': str(photowalk.id),
            'organizer_id': str(photowalk.organizer_id),
            'title': photowalk.title,
            'description': photowalk.description,
            'location': photowalk.location,
            'start_time': photowalk.start_time,
            'end_time': photowalk.end_time,
            'capacity': photowalk.capacity,
            'status': photowalk.status
        }
    }), 201


@bp.route('/<uuid:photowalk_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_photowalk(photowalk_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    photowalk, error = photowalk_service.get_by_id_for_user(
        photowalk_id=photowalk_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Photowalk not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this photowalk'
            )
        }), 403

    return jsonify({
        'id': str(photowalk.id),
        'organizer_id': str(photowalk.organizer_id),
        'title': photowalk.title,
        'description': photowalk.description,
        'location': photowalk.location,
        'start_time': photowalk.start_time,
        'end_time': photowalk.end_time,
        'capacity': photowalk.capacity,
        'status': photowalk.status
    }), 200


@bp.route('/<uuid:photowalk_id>', methods=['PUT'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def update_photowalk(photowalk_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    photowalk, error = photowalk_service.update(
        photowalk_id=photowalk_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Photowalk not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only update '
                'your own photowalks'
            )
        }), 403

    return jsonify({
        'message': 'Photowalk updated successfully',
        'photowalk': {
            'id': str(photowalk.id),
            'organizer_id': str(photowalk.organizer_id),
            'title': photowalk.title,
            'description': photowalk.description,
            'location': photowalk.location,
            'start_time': photowalk.start_time,
            'end_time': photowalk.end_time,
            'capacity': photowalk.capacity,
            'status': photowalk.status
        }
    }), 200


@bp.route('/<uuid:photowalk_id>', methods=['DELETE'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def delete_photowalk(photowalk_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = photowalk_service.delete(
        photowalk_id=photowalk_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Photowalk not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only delete '
                'your own photowalks'
            )
        }), 403

    return jsonify({
        'message': 'Photowalk deleted successfully'
    }), 200