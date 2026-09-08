import uuid

from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from infrastructure.databases.base import Base


class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )

    film_lab_id = Column(
        UUID(as_uuid=True),
        ForeignKey('film_labs.id'),
        nullable=False
    )

    service_id = Column(
        UUID(as_uuid=True),
        ForeignKey('services.id'),
        nullable=False
    )

    film_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey('film_types.id'),
        nullable=False
    )

    processing_options = Column(
        Text,
        nullable=True
    )

    scanning_quality = Column(
        Text,
        nullable=True
    )

    printing_requirements = Column(
        Text,
        nullable=True
    )

    additional_requests = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default='pending'
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
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