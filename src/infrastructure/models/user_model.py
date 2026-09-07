from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.databases.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    username = Column(
        String(50),
        nullable=False,
        unique=True
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=True
    )

    avatar_url = Column(
        String,
        nullable=True
    )

    role = Column(
        String(30),
        nullable=False,
        server_default=text("'customer'")
    )

    status = Column(
        String(20),
        nullable=False,
        server_default=text("'active'")
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text('now()')
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )