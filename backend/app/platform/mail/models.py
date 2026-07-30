from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.shared.base_model import BaseModel

if TYPE_CHECKING:
    from app.platform.tenants.models import Tenant


# ==========================================================
# CUSTOMER
# ==========================================================

class Customer(BaseModel):
    __tablename__ = "mail_customers"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    company: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship()

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )


# ==========================================================
# PRODUCT
# ==========================================================

class Product(BaseModel):
    __tablename__ = "mail_products"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    tenant: Mapped["Tenant"] = relationship()

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )


# ==========================================================
# ORDER
# ==========================================================

class Order(BaseModel):
    __tablename__ = "mail_orders"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    order_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending",
        nullable=False,
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        default="Pending",
        nullable=False,
    )

    payment_method: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    shipping_address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    courier: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    tax: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    shipping_charge: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    total: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tenant: Mapped["Tenant"] = relationship()

    customer: Mapped["Customer"] = relationship(
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    email_logs: Mapped[list["EmailLog"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )


# ==========================================================
# ORDER ITEM
# ==========================================================

class OrderItem(BaseModel):
    __tablename__ = "mail_order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    total_price: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )

# ==========================================================
# TICKET
# ==========================================================

class Ticket(BaseModel):
    __tablename__ = "mail_tickets"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    ticket_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        default="General",
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="Medium",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Open",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    assigned_to: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    resolved_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    tenant: Mapped["Tenant"] = relationship()

    order: Mapped["Order"] = relationship(
        back_populates="tickets",
    )


# ==========================================================
# CONVERSATION
# ==========================================================

class Conversation(BaseModel):
    __tablename__ = "mail_conversations"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        default="Email",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Open",
    )

    tenant: Mapped["Tenant"] = relationship()

    order: Mapped["Order"] = relationship(
        back_populates="conversations",
    )

    customer: Mapped["Customer"] = relationship()

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


# ==========================================================
# MESSAGE
# ==========================================================

class Message(BaseModel):
    __tablename__ = "mail_messages"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    sender: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    sender_type: Mapped[str] = mapped_column(
        String(50),
        default="Customer",
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    attachment_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )


# ==========================================================
# EMAIL LOG
# ==========================================================

class EmailLog(BaseModel):
    __tablename__ = "mail_email_logs"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "mail_orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    template_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Sent",
    )

    provider: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    provider_message_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sent_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    order: Mapped["Order"] = relationship(
        back_populates="email_logs",
    )

    tenant: Mapped["Tenant"] = relationship()
