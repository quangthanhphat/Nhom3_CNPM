from sqlalchemy import Column, String, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.databases.base import Base


class DigitalFilmArchiveModel(Base):
    __tablename__ = 'digital_film_archives'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    customer_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
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