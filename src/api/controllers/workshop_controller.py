from flask import Blueprint, jsonify, request

from services.workshop_service import WorkshopService
from api.middleware import token_required, role_required


bp = Blueprint(
    'workshop',
    __name__,
    url_prefix='/workshops'
)

workshop_service = WorkshopService()


# =========================
# GET ALL WORKSHOPS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_all_workshops():
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workshops = workshop_service.list_for_user(
        user_id=user_id,
        role=role
    )

    result = []

    for workshop in workshops:
        result.append({
            'id': str(workshop.id),
            'organizer_id': str(workshop.organizer_id),
            'title': workshop.title,
            'description': workshop.description,
            'location': workshop.location,
            'start_time': workshop.start_time,
            'end_time': workshop.end_time,
            'capacity': workshop.capacity,
            'status': workshop.status
        })

    return jsonify(result), 200


# =========================
# CREATE WORKSHOP
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def create_workshop():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    organizer_id = request.user.get('user_id')

    # Admin cũng dùng user hiện tại làm organizer
    workshop = workshop_service.create(
        organizer_id=organizer_id,
        data=data
    )

    return jsonify({
        'message': 'Workshop created successfully',
        'workshop': {
            'id': str(workshop.id),
            'organizer_id': str(workshop.organizer_id),
            'title': workshop.title,
            'description': workshop.description,
            'location': workshop.location,
            'start_time': workshop.start_time,
            'end_time': workshop.end_time,
            'capacity': workshop.capacity,
            'status': workshop.status
        }
    }), 201


# =========================
# GET WORKSHOP BY ID
# =========================

@bp.route('/<uuid:workshop_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'film_lab_owner',
    'photography_expert',
    'delivery_partner',
    'admin'
)
def get_workshop(workshop_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workshop, error = workshop_service.get_by_id_for_user(
        workshop_id=workshop_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Workshop not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You do not have permission '
                'to view this workshop'
            )
        }), 403

    return jsonify({
        'id': str(workshop.id),
        'organizer_id': str(workshop.organizer_id),
        'title': workshop.title,
        'description': workshop.description,
        'location': workshop.location,
        'start_time': workshop.start_time,
        'end_time': workshop.end_time,
        'capacity': workshop.capacity,
        'status': workshop.status
    }), 200


# =========================
# UPDATE WORKSHOP
# =========================

@bp.route('/<uuid:workshop_id>', methods=['PUT'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def update_workshop(workshop_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request'
        }), 400

    user_id = request.user.get('user_id')
    role = request.user.get('role')

    workshop, error = workshop_service.update(
        workshop_id=workshop_id,
        data=data,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Workshop not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only update '
                'your own workshops'
            )
        }), 403

    return jsonify({
        'message': 'Workshop updated successfully',
        'workshop': {
            'id': str(workshop.id),
            'organizer_id': str(workshop.organizer_id),
            'title': workshop.title,
            'description': workshop.description,
            'location': workshop.location,
            'start_time': workshop.start_time,
            'end_time': workshop.end_time,
            'capacity': workshop.capacity,
            'status': workshop.status
        }
    }), 200


# =========================
# DELETE WORKSHOP
# =========================

@bp.route('/<uuid:workshop_id>', methods=['DELETE'])
@token_required
@role_required(
    'photography_expert',
    'admin'
)
def delete_workshop(workshop_id):
    user_id = request.user.get('user_id')
    role = request.user.get('role')

    deleted, error = workshop_service.delete(
        workshop_id=workshop_id,
        user_id=user_id,
        role=role
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Workshop not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': (
                'You can only delete '
                'your own workshops'
            )
        }), 403

    return jsonify({
        'message': 'Workshop deleted successfully'
    }), 200