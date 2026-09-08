import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from infrastructure.databases.base import Base


class ArchiveItemModel(Base):
    __tablename__ = 'archive_items'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    archive_id = Column(
        UUID(as_uuid=True),
        ForeignKey('digital_film_archives.id'),
        nullable=False
    )

    scan_id = Column(
        UUID(as_uuid=True),
        ForeignKey('digital_scans.id'),
        nullable=False
    )

    added_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )