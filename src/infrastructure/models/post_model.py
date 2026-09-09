from infrastructure.databases.base import Base

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    text,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )

    type = Column(
        String(30),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default='published'
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )