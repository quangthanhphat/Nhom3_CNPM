import uuid

from sqlalchemy import Column, String, Text, Date, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from infrastructure.databases.base import Base


class DigitalScanModel(Base):
    __tablename__ = 'digital_scans'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('orders.id'),
        nullable=False
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    storage_path = Column(
        Text,
        nullable=False
    )

    file_size = Column(
        BigInteger,
        nullable=True
    )

    scan_specification = Column(
        Text,
        nullable=True
    )

    scan_quality = Column(
        Text,
        nullable=True
    )

    film_stock = Column(
        String(100),
        nullable=True
    )

    camera_model = Column(
        String(150),
        nullable=True
    )

    lens = Column(
        String(150),
        nullable=True
    )

    shooting_date = Column(
        Date,
        nullable=True
    )

    processing_method = Column(
        Text,
        nullable=True
    )

    uploaded_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )