from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

# ==========================================================
# CUSTOMER
# ==========================================================

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    company: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    company: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_active: bool | None = None


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime


# ==========================================================
# PRODUCT
# ==========================================================

class ProductBase(BaseModel):
    sku: str
    name: str
    description: str | None = None
    category: str | None = None
    price: float
    quantity: int
    image_url: str | None = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    quantity: int | None = None
    image_url: str | None = None
    is_active: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime


# ==========================================================
# ORDER ITEM
# ==========================================================

class OrderItemCreate(BaseModel):
    product_uuid: UUID
    quantity: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    quantity: int
    unit_price: float
    total_price: float

    product: ProductResponse


# ==========================================================
# ORDER
# ==========================================================

class OrderCreate(BaseModel):
    customer_uuid: UUID
    payment_method: str | None = None
    shipping_address: str | None = None
    notes: str | None = None
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: str | None = None
    payment_status: str | None = None
    payment_method: str | None = None
    shipping_address: str | None = None
    tracking_number: str | None = None
    courier: str | None = None
    notes: str | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID

    order_number: str

    status: str
    payment_status: str
    payment_method: str | None

    shipping_address: str | None

    tracking_number: str | None
    courier: str | None

    subtotal: float
    tax: float
    shipping_charge: float
    total: float

    notes: str | None

    created_at: datetime
    updated_at: datetime

    customer: CustomerResponse
    items: list[OrderItemResponse]

# ==========================================================
# TICKET
# ==========================================================

class TicketCreate(BaseModel):
    order_uuid: UUID
    subject: str
    category: str = "General"
    priority: str = "Medium"
    description: str


class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    assigned_to: str | None = None
    description: str | None = None


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID

    ticket_number: str

    subject: str
    category: str
    priority: str
    status: str

    description: str | None
    assigned_to: str | None

    created_at: datetime
    updated_at: datetime


# ==========================================================
# MESSAGE
# ==========================================================

class MessageCreate(BaseModel):
    sender: str
    sender_type: str
    message: str
    attachment_url: str | None = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID

    sender: str
    sender_type: str
    message: str

    attachment_url: str | None
    is_read: bool

    created_at: datetime


# ==========================================================
# CONVERSATION
# ==========================================================

class ConversationCreate(BaseModel):
    order_uuid: UUID
    customer_uuid: UUID
    subject: str
    channel: str = "Email"


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID

    subject: str
    channel: str
    status: str

    created_at: datetime
    updated_at: datetime

    messages: list[MessageResponse]


# ==========================================================
# EMAIL LOG
# ==========================================================

class EmailLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID

    recipient: str
    subject: str

    template_name: str | None

    provider: str | None
    provider_message_id: str | None

    status: str
    error_message: str | None

    sent_at: datetime | None


# ==========================================================
# DASHBOARD
# ==========================================================

class DashboardResponse(BaseModel):

    total_orders: int

    pending_orders: int

    delivered_orders: int

    cancelled_orders: int

    returned_orders: int

    refunded_orders: int

    total_customers: int

    total_products: int

    total_revenue: float

    open_tickets: int

    resolved_tickets: int

    emails_sent: int


# ==========================================================
# ORDER ACTIONS
# ==========================================================

class TrackingRequest(BaseModel):
    courier: str
    tracking_number: str


class ReturnRequest(BaseModel):
    reason: str


class ReplacementRequest(BaseModel):
    reason: str


class RefundRequest(BaseModel):
    amount: float
    reason: str


class CancelRequest(BaseModel):
    reason: str


class AddressUpdateRequest(BaseModel):
    shipping_address: str


# ==========================================================
# COMMON RESPONSE
# ==========================================================

class ActionResponse(BaseModel):
    success: bool
    message: str


class PaginationResponse(BaseModel):
    total: int
    page: int
    page_size: int


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    total: int


class ConversationListResponse(BaseModel):
    items: list[ConversationResponse]
    total: int


class EmailLogListResponse(BaseModel):
    items: list[EmailLogResponse]
    total: int 



class TestEmailRequest(BaseModel):
    senderEmail: EmailStr
    subject: str
    body: str


class TestEmailResponse(BaseModel):
    success: bool
    conversation_id: str
    reply: str