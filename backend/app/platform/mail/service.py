from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import HTTPException, status

from app.platform.mail.models import (
    Conversation,
    EmailLog,
    Message,
    Ticket,
)
from app.platform.mail.repository import MailRepository
from app.platform.mail.schemas import (
    AddressUpdateRequest,
    CancelRequest,
    ConversationCreate,
    CustomerCreate,
    CustomerUpdate,
    MessageCreate,
    OrderCreate,
    OrderUpdate,
    ProductCreate,
    ProductUpdate,
    RefundRequest,
    ReplacementRequest,
    ReturnRequest,
    TicketCreate,
    TicketUpdate,
    TrackingRequest,
)


class MailService:

    def __init__(self, repository: MailRepository):
        self.repo = repository

    # ======================================================
    # DASHBOARD
    # ======================================================

    def dashboard(self):
        return self.repo.dashboard()

    # ======================================================
    # CUSTOMERS
    # ======================================================

    def get_customers(self):
        return self.repo.get_customers()

    def get_customer(self, customer_uuid):

        customer = self.repo.get_customer(customer_uuid)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return customer

    def create_customer(
        self,
        data: CustomerCreate,
    ):
        return self.repo.create_customer(data)

    def update_customer(
        self,
        customer_uuid,
        data: CustomerUpdate,
    ):

        customer = self.get_customer(customer_uuid)

        return self.repo.update_customer(
            customer,
            data,
        )

    def delete_customer(
        self,
        customer_uuid,
    ):

        customer = self.get_customer(customer_uuid)

        self.repo.delete_customer(customer)

    # ======================================================
    # PRODUCTS
    # ======================================================

    def get_products(self):
        return self.repo.get_products()

    def get_product(self, product_uuid):

        product = self.repo.get_product(product_uuid)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    def create_product(
        self,
        data: ProductCreate,
    ):
        return self.repo.create_product(data)

    def update_product(
        self,
        product_uuid,
        data: ProductUpdate,
    ):

        product = self.get_product(product_uuid)

        return self.repo.update_product(
            product,
            data,
        )

    def delete_product(
        self,
        product_uuid,
    ):

        product = self.get_product(product_uuid)

        self.repo.delete_product(product)

    # ======================================================
    # ORDERS
    # ======================================================

    def get_orders(self):
        return self.repo.get_orders()

    def get_order(self, order_uuid):

        order = self.repo.get_order(order_uuid)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        return order

    def create_order(
        self,
        data: OrderCreate,
    ):

        customer = self.repo.get_customer(
            data.customer_uuid,
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        return self.repo.create_order(
            customer,
            data,
        )

    def update_order(
        self,
        order_uuid,
        data: OrderUpdate,
    ):

        order = self.get_order(order_uuid)

        return self.repo.update_order(
            order,
            data,
        )

    def update_address(
        self,
        order_uuid,
        data: AddressUpdateRequest,
    ):

        order = self.get_order(order_uuid)

        order.shipping_address = data.shipping_address

        self.repo.commit()

        return order
    
        # ======================================================
    # ORDER ACTIONS
    # ======================================================

    def track_order(
        self,
        order_uuid,
        data: TrackingRequest,
    ):

        order = self.get_order(order_uuid)

        return self.repo.update_tracking(
            order,
            data.courier,
            data.tracking_number,
        )

    def cancel_order(
        self,
        order_uuid,
        data: CancelRequest,
    ):

        order = self.get_order(order_uuid)

        order = self.repo.cancel_order(order)

        self._create_email_log(
            order,
            "Order Cancelled",
            f"Reason: {data.reason}",
        )

        return order

    def return_order(
        self,
        order_uuid,
        data: ReturnRequest,
    ):

        order = self.get_order(order_uuid)

        order = self.repo.return_order(order)

        self._create_ticket(
            order,
            "Return Request",
            data.reason,
        )

        return order

    def replacement_order(
        self,
        order_uuid,
        data: ReplacementRequest,
    ):

        order = self.get_order(order_uuid)

        order = self.repo.replace_order(order)

        self._create_ticket(
            order,
            "Replacement Request",
            data.reason,
        )

        return order

    def refund_order(
        self,
        order_uuid,
        data: RefundRequest,
    ):

        order = self.get_order(order_uuid)

        order = self.repo.refund_order(order)

        self._create_email_log(
            order,
            "Refund Initiated",
            f"Refund Amount: {data.amount}",
        )

        return order

    # ======================================================
    # TICKETS
    # ======================================================

    def get_tickets(self):
        return self.repo.get_tickets()

    def get_ticket(
        self,
        ticket_uuid,
    ):

        ticket = self.repo.get_ticket(ticket_uuid)

        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found",
            )

        return ticket

    def create_ticket(
        self,
        data: TicketCreate,
    ):

        order = self.get_order(
            data.order_uuid,
        )

        ticket = Ticket(
            tenant_id=self.repo.tenant_id,
            order_id=order.id,
            ticket_number=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            subject=data.subject,
            category=data.category,
            priority=data.priority,
            status="Open",
            description=data.description,
        )

        return self.repo.create_ticket(ticket)

    def update_ticket(
        self,
        ticket_uuid,
        data: TicketUpdate,
    ):

        ticket = self.get_ticket(ticket_uuid)

        values = data.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():
            setattr(ticket, key, value)

        return self.repo.update_ticket(ticket)

    # ======================================================
    # CONVERSATIONS
    # ======================================================

    def get_conversations(self):
        return self.repo.get_conversations()

    def get_conversation(
        self,
        conversation_uuid,
    ):

        conversation = self.repo.get_conversation(
            conversation_uuid
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        return conversation

    def create_conversation(
        self,
        data: ConversationCreate,
    ):

        customer = self.get_customer(
            data.customer_uuid,
        )

        order = self.get_order(
            data.order_uuid,
        )

        conversation = Conversation(
            tenant_id=self.repo.tenant_id,
            customer_id=customer.id,
            order_id=order.id,
            subject=data.subject,
            channel=data.channel,
            status="Open",
        )

        return self.repo.create_conversation(
            conversation,
        )

    def add_message(
        self,
        conversation_uuid,
        data: MessageCreate,
    ):

        conversation = self.get_conversation(
            conversation_uuid,
        )

        message = Message(
            conversation_id=conversation.id,
            sender=data.sender,
            sender_type=data.sender_type,
            message=data.message,
            attachment_url=data.attachment_url,
        )

        return self.repo.add_message(message)
    

        # ======================================================
    # EMAIL LOGS
    # ======================================================

    def get_email_logs(self):
        return self.repo.get_email_logs()

    def get_email_log(
        self,
        log_uuid,
    ):

        log = self.repo.get_email_log(log_uuid)

        if log is None:
            raise HTTPException(
                status_code=404,
                detail="Email log not found",
            )

        return log

    # ======================================================
    # GST INVOICE
    # ======================================================

    def generate_invoice(
        self,
        order_uuid,
    ):

        order = self.get_order(order_uuid)

        invoice = {
            "invoice_number": f"INV-{uuid.uuid4().hex[:8].upper()}",
            "generated_at": datetime.utcnow().isoformat(),
            "order_number": order.order_number,
            "customer": {
                "name": f"{order.customer.first_name} {order.customer.last_name}",
                "email": order.customer.email,
                "address": order.shipping_address,
            },
            "items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total": item.total_price,
                }
                for item in order.items
            ],
            "subtotal": order.subtotal,
            "tax": order.tax,
            "shipping": order.shipping_charge,
            "grand_total": order.total,
            "payment_status": order.payment_status,
            "status": order.status,
        }

        self._create_email_log(
            order,
            "GST Invoice Generated",
            invoice["invoice_number"],
        )

        return invoice

    # ======================================================
    # PRIVATE HELPERS
    # ======================================================

    def _create_ticket(
        self,
        order,
        subject: str,
        description: str,
    ):

        ticket = Ticket(
            tenant_id=self.repo.tenant_id,
            order_id=order.id,
            ticket_number=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            subject=subject,
            category="Order",
            priority="Medium",
            status="Open",
            description=description,
        )

        return self.repo.create_ticket(ticket)

    def _create_email_log(
        self,
        order,
        subject: str,
        template: str,
    ):

        log = EmailLog(
            tenant_id=self.repo.tenant_id,
            order_id=order.id,
            recipient=order.customer.email,
            subject=subject,
            template_name=template,
            provider="System",
            provider_message_id=str(uuid.uuid4()),
            status="Sent",
            sent_at=datetime.utcnow(),
        )

        return self.repo.create_email_log(log)

    # ======================================================
    # SEARCH
    # ======================================================

    def search_orders(
        self,
        keyword: str,
    ):
        return self.repo.search_orders(keyword)

    def search_customers(
        self,
        keyword: str,
    ):
        return self.repo.search_customers(keyword)

    # ======================================================
    # DELETE
    # ======================================================

    def delete_order(
        self,
        order_uuid,
    ):

        order = self.get_order(order_uuid)

        self.repo.delete_order(order)

    # ======================================================
    # HEALTH
    # ======================================================

    def ping(self):

        return {
            "status": "ok",
            "module": "mail",
            "tenant_id": self.repo.tenant_id,
        }
    

    def process_test_email(self, tenant_id: int, request: TestEmailRequest):

        customer = self.repository.get_customer_by_email(
            tenant_id,
            request.senderEmail,
        )

        if customer is None:
            raise ValueError("Customer not found.")

        conversation = Conversation(
            tenant_id=tenant_id,
            customer_id=customer.id,
            subject=request.subject,
            status="OPEN",
        )

        self.db.add(conversation)
        self.db.flush()

        message = Message(
            tenant_id=tenant_id,
            conversation_id=conversation.id,
            sender=request.senderEmail,
            body=request.body,
            direction="INBOUND",
        )

        self.db.add(message)

        email_log = EmailLog(
            tenant_id=tenant_id,
            recipient=request.senderEmail,
            subject=request.subject,
            template_name="TEST",
            status="RECEIVED",
            provider="SIMULATOR",
        )

        self.db.add(email_log)

        self.db.commit()

        return TestEmailResponse(
            ok=True,
            status="success",
            message="Test email processed successfully.",
        )