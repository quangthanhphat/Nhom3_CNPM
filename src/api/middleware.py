import os
from functools import wraps

import jwt
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'message': 'Authorization token is required'
            }), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'message': 'Invalid authorization format'
            }), 401

        token = parts[1]

        secret_key = os.environ.get(
            'SECRET_KEY',
            'film_lab_secret_key'
        )

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256']
            )

            request.user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Token has expired'
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                'message': 'Invalid token'
            }), 401

        return f(*args, **kwargs)

    return decorated