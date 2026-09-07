from flask import Blueprint, jsonify, request
from services.film_lab_service import FilmLabService
from api.middleware import token_required


bp = Blueprint(
    'film_lab',
    __name__,
    url_prefix='/film-labs'
)

film_lab_service = FilmLabService()


@bp.route('/', methods=['GET'])
@token_required
def get_all_film_labs():
    film_labs = film_lab_service.list_all()

    result = []

    for lab in film_labs:
        result.append({
            'id': str(lab.id),
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


@bp.route('/', methods=['POST'])
@token_required
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


@bp.route('/<uuid:film_lab_id>', methods=['PUT'])
@token_required
def update_film_lab(film_lab_id):
    data = request.get_json()

    film_lab = film_lab_service.update(
        film_lab_id=film_lab_id,
        data=data
    )

    if not film_lab:
        return jsonify({
            'message': 'Film lab not found'
        }), 404

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


@bp.route('/<uuid:film_lab_id>', methods=['DELETE'])
@token_required
def delete_film_lab(film_lab_id):
    deleted = film_lab_service.delete(film_lab_id)

    if not deleted:
        return jsonify({
            'message': 'Film lab not found'
        }), 404

    return jsonify({
        'message': 'Film lab deleted successfully'
    }), 200


@bp.route('/<uuid:film_lab_id>', methods=['GET'])
def get_film_lab(film_lab_id):
    lab = film_lab_service.get_by_id(film_lab_id)

    if not lab:
        return jsonify({
            'message': 'Film lab not found'
        }), 404

    return jsonify({
        'id': str(lab.id),
        'name': lab.name,
        'description': lab.description,
        'city': lab.city,
        'district': lab.district,
        'address': lab.address,
        'phone': lab.phone,
        'email': lab.email,
        'status': lab.status
    }), 200