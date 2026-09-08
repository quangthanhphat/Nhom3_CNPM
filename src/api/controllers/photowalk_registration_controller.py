from flask import Blueprint, jsonify, request

from services.photowalk_registration_service import (
    PhotowalkRegistrationService
)
from api.middleware import token_required, role_required


bp = Blueprint(
    'photowalk_registration',
    __name__,
    url_prefix='/photowalk-registrations'
)

photowalk_registration_service = PhotowalkRegistrationService()


@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def get_all_registrations():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    registrations = photowalk_registration_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for registration in registrations:
        result.append({
            'id': str(registration.id),
            'photowalk_id': str(registration.photowalk_id),
            'user_id': str(registration.user_id),
            'registered_at': registration.registered_at
        })

    return jsonify(result), 200


@bp.route('/', methods=['POST'])
@token_required
@role_required('customer')
def create_registration():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    if not data.get('photowalk_id'):
        return jsonify({
            'message': 'photowalk_id is required'
        }), 400

    user_id = request.user.get('user_id')

    registration, error = photowalk_registration_service.create(
        user_id=user_id,
        data=data
    )

    if error == 'photowalk_not_found':
        return jsonify({
            'message': 'Photowalk not found'
        }), 404

    return jsonify({
        'message': 'Photowalk registration created successfully',
        'registration': {
            'id': str(registration.id),
            'photowalk_id': str(registration.photowalk_id),
            'user_id': str(registration.user_id),
            'registered_at': registration.registered_at
        }
    }), 201


@bp.route('/<uuid:registration_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def get_registration(registration_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    registration, error = (
        photowalk_registration_service.get_by_id_for_user(
            registration_id=registration_id,
            user_id=user_id,
            role=role
        )
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Photowalk registration not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this registration'
            )
        }), 403

    return jsonify({
        'id': str(registration.id),
        'photowalk_id': str(registration.photowalk_id),
        'user_id': str(registration.user_id),
        'registered_at': registration.registered_at
    }), 200


@bp.route('/<uuid:registration_id>', methods=['DELETE'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'admin'
)
def delete_registration(registration_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = photowalk_registration_service.delete(
        registration_id=registration_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Photowalk registration not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to delete this registration'
            )
        }), 403

    return jsonify({
        'message': 'Photowalk registration deleted successfully'
    }), 200