from flask import Blueprint, jsonify
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