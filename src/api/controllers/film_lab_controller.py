from flask import Blueprint, jsonify, request

from services.film_lab_service import FilmLabService
from api.middleware import token_required, role_required


bp = Blueprint(
    'film_lab',
    __name__,
    url_prefix='/film-labs'
)

film_lab_service = FilmLabService()


# =========================
# GET ALL FILM LABS
# =========================

@bp.route('/', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'film_lab_owner',
    'admin'
)
def get_all_film_labs():
    film_labs = film_lab_service.list_all()

    result = []

    for lab in film_labs:
        result.append({
            'id': str(lab.id),
            'owner_id': str(lab.owner_id),
            'name': lab.name,
            'description': lab.description,
            'city': lab.city,
            'district': lab.district,
            'address': lab.address,
            'phone': lab.phone,
            'email': lab.email,
            'status': lab.status
        })

    return jsonify(result), 200


# =========================
# CREATE FILM LAB
# =========================

@bp.route('/', methods=['POST'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def create_film_lab():
    data = request.get_json()

    user_id = request.user.get('user_id')

    film_lab = film_lab_service.create(
        owner_id=user_id,
        data=data
    )

    return jsonify({
        'message': 'Film lab created successfully',
        'film_lab': {
            'id': str(film_lab.id),
            'owner_id': str(film_lab.owner_id),
            'name': film_lab.name,
            'description': film_lab.description,
            'city': film_lab.city,
            'district': film_lab.district,
            'address': film_lab.address,
            'phone': film_lab.phone,
            'email': film_lab.email,
            'status': film_lab.status
        }
    }), 201


# =========================
# UPDATE FILM LAB
# =========================

@bp.route('/<uuid:film_lab_id>', methods=['PUT'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def update_film_lab(film_lab_id):
    data = request.get_json()

    user_id = request.user.get('user_id')
    is_admin = request.user.get('role') == 'admin'

    film_lab, error = film_lab_service.update(
        film_lab_id=film_lab_id,
        data=data,
        user_id=user_id,
        is_admin=is_admin
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Film lab not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only update your own film lab'
        }), 403

    return jsonify({
        'message': 'Film lab updated successfully',
        'film_lab': {
            'id': str(film_lab.id),
            'owner_id': str(film_lab.owner_id),
            'name': film_lab.name,
            'description': film_lab.description,
            'city': film_lab.city,
            'district': film_lab.district,
            'address': film_lab.address,
            'phone': film_lab.phone,
            'email': film_lab.email,
            'status': film_lab.status
        }
    }), 200


# =========================
# DELETE FILM LAB
# =========================

@bp.route('/<uuid:film_lab_id>', methods=['DELETE'])
@token_required
@role_required(
    'film_lab_owner',
    'admin'
)
def delete_film_lab(film_lab_id):
    user_id = request.user.get('user_id')
    is_admin = request.user.get('role') == 'admin'

    deleted, error = film_lab_service.delete(
        film_lab_id=film_lab_id,
        user_id=user_id,
        is_admin=is_admin
    )

    if error == 'not_found':
        return jsonify({
            'message': 'Film lab not found'
        }), 404

    if error == 'forbidden':
        return jsonify({
            'message': 'You can only delete your own film lab'
        }), 403

    return jsonify({
        'message': 'Film lab deleted successfully'
    }), 200


# =========================
# GET FILM LAB BY ID
# =========================

@bp.route('/<uuid:film_lab_id>', methods=['GET'])
@token_required
@role_required(
    'customer',
    'photography_expert',
    'film_lab_owner',
    'admin'
)
def get_film_lab(film_lab_id):
    lab = film_lab_service.get_by_id(film_lab_id)

    if not lab:
        return jsonify({
            'message': 'Film lab not found'
        }), 404

    return jsonify({
        'id': str(lab.id),
        'owner_id': str(lab.owner_id),
        'name': lab.name,
        'description': lab.description,
        'city': lab.city,
        'district': lab.district,
        'address': lab.address,
        'phone': lab.phone,
        'email': lab.email,
        'status': lab.status
    }), 200