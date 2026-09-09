from flask import Blueprint, request, jsonify

from services.auth_service import AuthService
from api.middleware import token_required


bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService()


def serialize_user(user):
    return {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'avatar_url': user.avatar_url,
        'role': user.role,
        'status': user.status
    }


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = auth_service.register(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        role='film_lab_owner'
    )

    if not user:
        return jsonify({
            'message': 'Username or email already exists'
        }), 409

    return jsonify({
        'message': 'Registration successful',
        'user': serialize_user(user)
    }), 201


@bp.route('/mobile-register', methods=['POST'])
def mobile_register():
    data = request.get_json()

    role = data.get('role')

    # Mobile chỉ cho phép Customer
    # hoặc Photography Expert đăng ký.
    if role not in [
        'customer',
        'photography_expert'
    ]:
        return jsonify({
            'message': 'Invalid registration role'
        }), 400

    user = auth_service.register(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        role=role
    )

    if not user:
        return jsonify({
            'message': 'Username or email already exists'
        }), 409

    return jsonify({
        'message': 'Registration successful',
        'user': serialize_user(user)
    }), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    result = auth_service.login(
        username=data.get('username'),
        password=data.get('password')
    )

    if not result:
        return jsonify({
            'message': 'Invalid username or password'
        }), 401

    user, token = result

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': serialize_user(user)
    }), 200


@bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    user_id = request.user.get('user_id')

    user = auth_service.get_user_by_id(user_id)

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    return jsonify({
        'user': serialize_user(user)
    }), 200


@bp.route('/me', methods=['PUT'])
@token_required
def update_current_user():
    data = request.get_json() or {}

    user_id = request.user.get('user_id')

    user, error = auth_service.update_profile(
        user_id,
        data
    )

    if error == 'not_found':
        return jsonify({
            'message': 'User not found'
        }), 404

    if error == 'email_exists':
        return jsonify({
            'message': 'Email already exists'
        }), 409

    return jsonify({
        'message': 'Profile updated successfully',
        'user': serialize_user(user)
    }), 200