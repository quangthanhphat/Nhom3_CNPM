from flask import Blueprint, jsonify, request

from api.middleware import token_required
from services.events_service import EventsService

bp = Blueprint('events', __name__, url_prefix='/events')
events_service = None


def _service():
    global events_service
    if events_service is None:
        events_service = EventsService()
    return events_service


def _user_id(): return request.user.get('user_id')

def _event(event, kind):
    result = {'id': str(event.id), 'organizer_id': str(event.organizer_id),
              'title': event.title, 'start_time': event.start_time.isoformat(),
              'end_time': event.end_time.isoformat() if event.end_time else None,
              'status': event.status, 'description': event.description,
              'created_at': event.created_at.isoformat() if event.created_at else None}
    result['location' if kind == 'workshop' else 'meeting_location'] = (event.location if kind == 'workshop' else event.meeting_location)
    return result


def _registration(registration, kind):
    event_key = 'workshop_id' if kind == 'workshop' else 'photowalk_id'
    return {'id': str(registration.id), event_key: str(getattr(registration, event_key)),
            'user_id': str(registration.user_id), 'status': registration.status,
            'registered_at': registration.registered_at.isoformat() if registration.registered_at else None,
            'cancelled_at': registration.cancelled_at.isoformat() if registration.cancelled_at else None}


def _error(error, status=400): return jsonify({'message': str(error)}), status


@bp.route('/workshops', methods=['GET'])
def list_workshops():
    return jsonify([_event(item, 'workshop') for item in _service().list_workshops(request.args.get('status'))]), 200

@bp.route('/workshops/<uuid:event_id>', methods=['GET'])
def get_workshop(event_id):
    item = _service().get_workshop(event_id)
    return (jsonify(_event(item, 'workshop')), 200) if item else _error('Workshop not found', 404)

@bp.route('/workshops', methods=['POST'])
@token_required
def create_workshop():
    try: return jsonify(_event(_service().create_workshop(_user_id(), request.get_json(silent=True) or {}), 'workshop')), 201
    except ValueError as error: return _error(error)

@bp.route('/workshops/<uuid:event_id>', methods=['PATCH'])
@token_required
def update_workshop(event_id):
    try:
        item = _service().update_workshop(event_id, _user_id(), request.get_json(silent=True) or {})
        return (jsonify(_event(item, 'workshop')), 200) if item else _error('Workshop not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error)

@bp.route('/workshops/<uuid:event_id>', methods=['DELETE'])
@token_required
def delete_workshop(event_id):
    try:
        return (jsonify({'message': 'Workshop deleted'}), 200) if _service().delete_workshop(event_id, _user_id()) else _error('Workshop not found', 404)
    except PermissionError as error: return _error(error, 403)

@bp.route('/workshops/<uuid:event_id>/registrations', methods=['GET'])
def list_workshop_registrations(event_id):
    registrations = _service().list_workshop_registrations(event_id)
    return (jsonify([_registration(item, 'workshop') for item in registrations]), 200) if registrations is not None else _error('Workshop not found', 404)

@bp.route('/workshops/<uuid:event_id>/registrations', methods=['POST'])
@token_required
def register_workshop(event_id):
    try:
        item = _service().register_workshop(event_id, _user_id())
        return (jsonify(_registration(item, 'workshop')), 201) if item else _error('Workshop not found', 404)
    except RuntimeError as error: return _error(error, 409)
    except ValueError as error: return _error(error)

@bp.route('/workshops/<uuid:event_id>/registrations', methods=['DELETE'])
@token_required
def cancel_workshop(event_id):
    try:
        return (jsonify({'message': 'Workshop registration cancelled'}), 200) if _service().cancel_workshop(event_id, _user_id()) else _error('Registration not found', 404)
    except ValueError as error: return _error(error)


@bp.route('/photowalks', methods=['GET'])
def list_photowalks():
    return jsonify([_event(item, 'photowalk') for item in _service().list_photowalks(request.args.get('status'))]), 200

@bp.route('/photowalks/<uuid:event_id>', methods=['GET'])
def get_photowalk(event_id):
    item = _service().get_photowalk(event_id)
    return (jsonify(_event(item, 'photowalk')), 200) if item else _error('Photowalk not found', 404)

@bp.route('/photowalks', methods=['POST'])
@token_required
def create_photowalk():
    try: return jsonify(_event(_service().create_photowalk(_user_id(), request.get_json(silent=True) or {}), 'photowalk')), 201
    except ValueError as error: return _error(error)

@bp.route('/photowalks/<uuid:event_id>', methods=['PATCH'])
@token_required
def update_photowalk(event_id):
    try:
        item = _service().update_photowalk(event_id, _user_id(), request.get_json(silent=True) or {})
        return (jsonify(_event(item, 'photowalk')), 200) if item else _error('Photowalk not found', 404)
    except PermissionError as error: return _error(error, 403)
    except ValueError as error: return _error(error)

@bp.route('/photowalks/<uuid:event_id>', methods=['DELETE'])
@token_required
def delete_photowalk(event_id):
    try:
        return (jsonify({'message': 'Photowalk deleted'}), 200) if _service().delete_photowalk(event_id, _user_id()) else _error('Photowalk not found', 404)
    except PermissionError as error: return _error(error, 403)

@bp.route('/photowalks/<uuid:event_id>/registrations', methods=['GET'])
def list_photowalk_registrations(event_id):
    registrations = _service().list_photowalk_registrations(event_id)
    return (jsonify([_registration(item, 'photowalk') for item in registrations]), 200) if registrations is not None else _error('Photowalk not found', 404)

@bp.route('/photowalks/<uuid:event_id>/registrations', methods=['POST'])
@token_required
def register_photowalk(event_id):
    try:
        item = _service().register_photowalk(event_id, _user_id())
        return (jsonify(_registration(item, 'photowalk')), 201) if item else _error('Photowalk not found', 404)
    except RuntimeError as error: return _error(error, 409)
    except ValueError as error: return _error(error)

@bp.route('/photowalks/<uuid:event_id>/registrations', methods=['DELETE'])
@token_required
def cancel_photowalk(event_id):
    try:
        return (jsonify({'message': 'Photowalk registration cancelled'}), 200) if _service().cancel_photowalk(event_id, _user_id()) else _error('Registration not found', 404)
    except ValueError as error: return _error(error)
