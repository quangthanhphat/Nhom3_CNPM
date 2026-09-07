from flask import Blueprint, request, jsonify
from services.auth_service import AuthService


bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService()


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = auth_service.register(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        phone=data.get('phone')
    )

    if not user:
        return jsonify({
            'message': 'Username or email already exists'
        }), 409

    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'role': user.role,
            'status': user.status
        }
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
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'role': user.role,
            'status': user.status
        }
    }), 200