import os
import sys

# Thêm thư mục src vào Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.models.user_model import UserModel
from infrastructure.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash


def create_admin():
    repository = UserRepository()

    username = 'admin'
    email = 'admin@filmlab.com'
    password = 'admin'

    existing_user = repository.find_by_username(username)

    if existing_user:
        print('Admin account already exists.')
        return

    password_hash = generate_password_hash(password)

    admin = UserModel(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name='Administrator',
        role='admin',
        status='active'
    )

    repository.create(admin)

    print('Admin account created successfully!')
    print('Username: admin')
    print('Password: admin')


if __name__ == '__main__':
    create_admin()