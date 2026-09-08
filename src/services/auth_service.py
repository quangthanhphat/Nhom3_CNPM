import os
from datetime import datetime, timedelta, timezone

import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from infrastructure.models.user_model import UserModel
from infrastructure.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def register(
        self,
        username,
        email,
        password,
        full_name,
        phone=None,
        role='customer'
    ):
        if self.repository.find_by_username(username):
            return None

        if self.repository.find_by_email(email):
            return None

        # Chỉ cho phép các role được đăng ký
        if role not in [
            'customer',
            'film_lab_owner',
            'photography_expert'
        ]:
            return None

        password_hash = generate_password_hash(password)

        user = UserModel(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            phone=phone,
            role=role
        )

        return self.repository.create(user)

    def login(self, username, password):
        user = self.repository.find_by_username(username)

        if not user:
            return None

        if not check_password_hash(
            user.password_hash,
            password
        ):
            return None

        token = self._create_token(user)

        return user, token

    def _create_token(self, user):
        secret_key = os.environ.get(
            'SECRET_KEY',
            'film_lab_secret_key'
        )

        payload = {
            'user_id': str(user.id),
            'username': user.username,
            'role': user.role,
            'exp': datetime.now(timezone.utc)
            + timedelta(hours=24)
        }

        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )