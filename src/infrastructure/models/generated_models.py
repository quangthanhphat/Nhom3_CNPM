from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.databases.base import Base


class Complaints(Base):
    __tablename__ = 'complaints'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='complaints_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'open'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    resolution: Mapped[Optional[str]] = mapped_column(Text)
    resolved_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DigitalFilmArchives(Base):
    __tablename__ = 'digital_film_archives'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='digital_film_archives_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    customer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    archive_items: Mapped[list['ArchiveItems']] = relationship('ArchiveItems', back_populates='archive')


class Favorites(Base):
    __tablename__ = 'favorites'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='favorites_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    target_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))


class FilmLabs(Base):
    __tablename__ = 'film_labs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='film_labs_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    district: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    services: Mapped[list['Services']] = relationship('Services', back_populates='film_lab')
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='film_lab')


class FilmTypes(Base):
    __tablename__ = 'film_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='film_types_pkey'),
        UniqueConstraint('name', name='film_types_name_key'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='film_type')


class MarketplaceListings(Base):
    __tablename__ = 'marketplace_listings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='marketplace_listings_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    seller_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    condition: Mapped[Optional[str]] = mapped_column(String(30))
    image_path: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    marketplace_messages: Mapped[list['MarketplaceMessages']] = relationship('MarketplaceMessages', back_populates='listing')
    marketplace_transactions: Mapped[list['MarketplaceTransactions']] = relationship('MarketplaceTransactions', back_populates='listing')


class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='notifications_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))


class Photowalks(Base):
    __tablename__ = 'photowalks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='photowalks_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    organizer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'upcoming'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    meeting_location: Mapped[Optional[str]] = mapped_column(Text)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    photowalk_registrations: Mapped[list['PhotowalkRegistrations']] = relationship('PhotowalkRegistrations', back_populates='photowalk')


class Posts(Base):
    __tablename__ = 'posts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='posts_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    author_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'published'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    comments: Mapped[list['Comments']] = relationship('Comments', back_populates='post')
    knowledge_base: Mapped[list['KnowledgeBase']] = relationship('KnowledgeBase', back_populates='post')


class Ratings(Base):
    __tablename__ = 'ratings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ratings_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    target_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    review: Mapped[Optional[str]] = mapped_column(Text)


class ServiceCategories(Base):
    __tablename__ = 'service_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='service_categories_pkey'),
        UniqueConstraint('name', name='service_categories_name_key'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    services: Mapped[list['Services']] = relationship('Services', back_populates='category')


class TransactionFees(Base):
    __tablename__ = 'transaction_fees'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='transaction_fees_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    fee_type: Mapped[str] = mapped_column(String(30), nullable=False)
    fee_value: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'customer'::character varying"))
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Workshops(Base):
    __tablename__ = 'workshops'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='workshops_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    organizer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'upcoming'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(Text)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    workshop_registrations: Mapped[list['WorkshopRegistrations']] = relationship('WorkshopRegistrations', back_populates='workshop')


class Comments(Base):
    __tablename__ = 'comments'
    __table_args__ = (
        ForeignKeyConstraint(['post_id'], ['public.posts.id'], name='comments_post_id_fkey'),
        PrimaryKeyConstraint('id', name='comments_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    post_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    post: Mapped['Posts'] = relationship('Posts', back_populates='comments')


class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    __table_args__ = (
        ForeignKeyConstraint(['post_id'], ['public.posts.id'], name='knowledge_base_post_id_fkey'),
        PrimaryKeyConstraint('id', name='knowledge_base_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    author_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'published'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    post_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    post: Mapped[Optional['Posts']] = relationship('Posts', back_populates='knowledge_base')


class MarketplaceMessages(Base):
    __tablename__ = 'marketplace_messages'
    __table_args__ = (
        ForeignKeyConstraint(['listing_id'], ['public.marketplace_listings.id'], name='marketplace_messages_listing_id_fkey'),
        PrimaryKeyConstraint('id', name='marketplace_messages_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    listing_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    sender_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    receiver_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    listing: Mapped['MarketplaceListings'] = relationship('MarketplaceListings', back_populates='marketplace_messages')


class MarketplaceTransactions(Base):
    __tablename__ = 'marketplace_transactions'
    __table_args__ = (
        ForeignKeyConstraint(['listing_id'], ['public.marketplace_listings.id'], name='marketplace_transactions_listing_id_fkey'),
        PrimaryKeyConstraint('id', name='marketplace_transactions_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    listing_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    buyer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    seller_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    listing: Mapped['MarketplaceListings'] = relationship('MarketplaceListings', back_populates='marketplace_transactions')


class PhotowalkRegistrations(Base):
    __tablename__ = 'photowalk_registrations'
    __table_args__ = (
        ForeignKeyConstraint(['photowalk_id'], ['public.photowalks.id'], name='photowalk_registrations_photowalk_id_fkey'),
        PrimaryKeyConstraint('id', name='photowalk_registrations_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    photowalk_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'registered'::character varying"))
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    cancelled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    photowalk: Mapped['Photowalks'] = relationship('Photowalks', back_populates='photowalk_registrations')


class Services(Base):
    __tablename__ = 'services'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['public.service_categories.id'], name='services_category_id_fkey'),
        ForeignKeyConstraint(['film_lab_id'], ['public.film_labs.id'], name='services_film_lab_id_fkey'),
        PrimaryKeyConstraint('id', name='services_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    film_lab_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    turnaround_time: Mapped[Optional[int]] = mapped_column(Integer)
    processing_capacity: Mapped[Optional[int]] = mapped_column(Integer)
    supported_film_formats: Mapped[Optional[str]] = mapped_column(Text)
    processing_options: Mapped[Optional[str]] = mapped_column(Text)
    scanning_quality: Mapped[Optional[str]] = mapped_column(Text)
    printing_options: Mapped[Optional[str]] = mapped_column(Text)
    specialized_techniques: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    category: Mapped['ServiceCategories'] = relationship('ServiceCategories', back_populates='services')
    film_lab: Mapped['FilmLabs'] = relationship('FilmLabs', back_populates='services')
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='service')


class WorkshopRegistrations(Base):
    __tablename__ = 'workshop_registrations'
    __table_args__ = (
        ForeignKeyConstraint(['workshop_id'], ['public.workshops.id'], name='workshop_registrations_workshop_id_fkey'),
        PrimaryKeyConstraint('id', name='workshop_registrations_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    workshop_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'registered'::character varying"))
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    cancelled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    workshop: Mapped['Workshops'] = relationship('Workshops', back_populates='workshop_registrations')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['film_lab_id'], ['public.film_labs.id'], name='orders_film_lab_id_fkey'),
        ForeignKeyConstraint(['film_type_id'], ['public.film_types.id'], name='orders_film_type_id_fkey'),
        ForeignKeyConstraint(['service_id'], ['public.services.id'], name='orders_service_id_fkey'),
        PrimaryKeyConstraint('id', name='orders_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    customer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    film_lab_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    service_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    film_type_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'pending'::character varying"))
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    processing_options: Mapped[Optional[str]] = mapped_column(Text)
    scanning_quality: Mapped[Optional[str]] = mapped_column(Text)
    printing_requirements: Mapped[Optional[str]] = mapped_column(Text)
    additional_requests: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    film_lab: Mapped['FilmLabs'] = relationship('FilmLabs', back_populates='orders')
    film_type: Mapped['FilmTypes'] = relationship('FilmTypes', back_populates='orders')
    service: Mapped['Services'] = relationship('Services', back_populates='orders')
    deliveries: Mapped[list['Deliveries']] = relationship('Deliveries', back_populates='order')
    digital_scans: Mapped[list['DigitalScans']] = relationship('DigitalScans', back_populates='order')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='order')
    processing_workflows: Mapped[list['ProcessingWorkflows']] = relationship('ProcessingWorkflows', back_populates='order')


class Deliveries(Base):
    __tablename__ = 'deliveries'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.id'], name='deliveries_order_id_fkey'),
        PrimaryKeyConstraint('id', name='deliveries_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    delivery_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    delivery_partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    pickup_address: Mapped[Optional[str]] = mapped_column(Text)
    destination_address: Mapped[Optional[str]] = mapped_column(Text)
    external_delivery_reference: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    order: Mapped['Orders'] = relationship('Orders', back_populates='deliveries')


class DigitalScans(Base):
    __tablename__ = 'digital_scans'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.id'], name='digital_scans_order_id_fkey'),
        PrimaryKeyConstraint('id', name='digital_scans_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    scan_specification: Mapped[Optional[str]] = mapped_column(Text)
    scan_quality: Mapped[Optional[str]] = mapped_column(Text)
    film_stock: Mapped[Optional[str]] = mapped_column(String(100))
    camera_model: Mapped[Optional[str]] = mapped_column(String(150))
    lens: Mapped[Optional[str]] = mapped_column(String(150))
    shooting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    processing_method: Mapped[Optional[str]] = mapped_column(Text)

    order: Mapped['Orders'] = relationship('Orders', back_populates='digital_scans')
    archive_items: Mapped[list['ArchiveItems']] = relationship('ArchiveItems', back_populates='scan')


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.id'], name='payments_order_id_fkey'),
        PrimaryKeyConstraint('id', name='payments_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(255))
    paid_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    order: Mapped['Orders'] = relationship('Orders', back_populates='payments')


class ProcessingWorkflows(Base):
    __tablename__ = 'processing_workflows'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['public.orders.id'], name='processing_workflows_order_id_fkey'),
        PrimaryKeyConstraint('id', name='processing_workflows_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    order: Mapped['Orders'] = relationship('Orders', back_populates='processing_workflows')


class ArchiveItems(Base):
    __tablename__ = 'archive_items'
    __table_args__ = (
        ForeignKeyConstraint(['archive_id'], ['public.digital_film_archives.id'], name='archive_items_archive_id_fkey'),
        ForeignKeyConstraint(['scan_id'], ['public.digital_scans.id'], name='archive_items_scan_id_fkey'),
        PrimaryKeyConstraint('id', name='archive_items_pkey'),
        {'schema': 'public'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    archive_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    scan_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    archive: Mapped['DigitalFilmArchives'] = relationship('DigitalFilmArchives', back_populates='archive_items')
    scan: Mapped['DigitalScans'] = relationship('DigitalScans', back_populates='archive_items')
