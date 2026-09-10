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


class SupportModel(Base):
    __tablename__ = 'support_tickets'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )

    subject = Column(
        String(200),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    reply = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(20),
        nullable=False,
        default='open'
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