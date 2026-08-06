from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.platform.mail.models import (
    Conversation,
    Customer,
    EmailLog,
    Message,
    Order,
    OrderItem,
    Product,
    Ticket,
)
from app.platform.mail.schemas import (
    CustomerCreate,
    CustomerUpdate,
    OrderCreate,
    OrderUpdate,
    ProductCreate,
    ProductUpdate,
)


class MailRepository:

    def __init__(
        self,
        db: Session,
        tenant_id: int,
    ):
        self.db = db
        self.tenant_id = tenant_id

    # =========================================================
    # CUSTOMER
    # =========================================================

    def get_customers(self):

        stmt = (
            select(Customer)
            .where(Customer.tenant_id == self.tenant_id)
            .order_by(Customer.created_at.desc())
        )

        return self.db.scalars(stmt).all()

    def get_customer(
        self,
        customer_uuid: UUID,
    ):

        stmt = (
            select(Customer)
            .where(
                Customer.uuid == customer_uuid,
                Customer.tenant_id == self.tenant_id,
            )
        )

        return self.db.scalar(stmt)

    def get_customer_by_email(
        self,
        email: str,
    ):
        print("Tenant ID:", self.tenant_id)
        print("Email:", email)

        stmt = (
            select(Customer)
            .where(
                Customer.email == email,
                Customer.tenant_id == self.tenant_id,
            )
        )

        customer = self.db.scalar(stmt)

        print("DB Result:", customer)

        return customer

    def create_customer(
        self,
        data: CustomerCreate,
    ):

        customer = Customer(
            tenant_id=self.tenant_id,
            **data.model_dump(),
        )

        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def update_customer(
        self,
        customer: Customer,
        data: CustomerUpdate,
    ):

        values = data.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)

        return customer

    def delete_customer(
        self,
        customer: Customer,
    ):

        self.db.delete(customer)
        self.db.commit()

    # =========================================================
    # PRODUCT
    # =========================================================

    def get_products(self):

        stmt = (
            select(Product)
            .where(
                Product.tenant_id == self.tenant_id
            )
            .order_by(Product.created_at.desc())
        )

        return self.db.scalars(stmt).all()

    def get_product(
        self,
        product_uuid: UUID,
    ):

        stmt = (
            select(Product)
            .where(
                Product.uuid == product_uuid,
                Product.tenant_id == self.tenant_id,
            )
        )

        return self.db.scalar(stmt)

    def create_product(
        self,
        data: ProductCreate,
    ):

        product = Product(
            tenant_id=self.tenant_id,
            **data.model_dump(),
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def update_product(
        self,
        product: Product,
        data: ProductUpdate,
    ):

        values = data.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)

        return product

    def delete_product(
        self,
        product: Product,
    ):

        self.db.delete(product)
        self.db.commit()

    # =========================================================
    # ORDER
    # =========================================================

    def get_orders(self):

        stmt = (
            select(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items).joinedload(
                    OrderItem.product
                ),
            )
            .where(
                Order.tenant_id == self.tenant_id
            )
            .order_by(Order.created_at.desc())
        )

        return (
            self.db.execute(stmt)
            .unique()
            .scalars()
            .all()
        )

    def get_order(
        self,
        order_uuid: UUID,
    ):

        stmt = (
            select(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items).joinedload(
                    OrderItem.product
                ),
                joinedload(Order.tickets),
                joinedload(Order.email_logs),
                joinedload(Order.conversations),
            )
            .where(
                Order.uuid == order_uuid,
                Order.tenant_id == self.tenant_id,
            )
        )

        return (
            self.db.execute(stmt)
            .unique()
            .scalar_one_or_none()
        )

    def create_order(
        self,
        customer: Customer,
        data: OrderCreate,
    ):

        order = Order(
            tenant_id=self.tenant_id,
            customer_id=customer.id,
            order_number=f"ORD-{customer.id}-{func.random()}",
            payment_method=data.payment_method,
            shipping_address=data.shipping_address,
            notes=data.notes,
            status="Pending",
            payment_status="Pending",
        )

        self.db.add(order)
        self.db.flush()

        subtotal = 0.0

        for item in data.items:

            product = self.get_product(
                item.product_uuid,
            )

            line_total = (
                product.price * item.quantity
            )

            subtotal += line_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                total_price=line_total,
            )

            self.db.add(order_item)

        order.subtotal = subtotal
        order.tax = subtotal * 0.18
        order.shipping_charge = 0
        order.total = (
            order.subtotal
            + order.tax
            + order.shipping_charge
        )

        self.db.commit()
        self.db.refresh(order)

        return order

    def update_order(
        self,
        order: Order,
        data: OrderUpdate,
    ):

        values = data.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():
            setattr(order, key, value)

        self.db.commit()
        self.db.refresh(order)

        return order

    def delete_order(
        self,
        order: Order,
    ):

        self.db.delete(order)
        self.db.commit()
    
        # =========================================================
    # TICKETS
    # =========================================================

    def get_tickets(self):

        stmt = (
            select(Ticket)
            .where(
                Ticket.tenant_id == self.tenant_id
            )
            .order_by(Ticket.created_at.desc())
        )

        return self.db.scalars(stmt).all()

    def get_ticket(
        self,
        ticket_uuid: UUID,
    ):

        stmt = (
            select(Ticket)
            .where(
                Ticket.uuid == ticket_uuid,
                Ticket.tenant_id == self.tenant_id,
            )
        )

        return self.db.scalar(stmt)

    def create_ticket(self, ticket: Ticket):

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)

        return ticket

    def update_ticket(self, ticket: Ticket):

        self.db.commit()
        self.db.refresh(ticket)

        return ticket

    def delete_ticket(self, ticket: Ticket):

        self.db.delete(ticket)
        self.db.commit()

    # =========================================================
    # CONVERSATIONS
    # =========================================================

    def get_conversations(self):

        stmt = (
            select(Conversation)
            .options(
                joinedload(
                    Conversation.messages
                )
            )
            .where(
                Conversation.tenant_id == self.tenant_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
        )

        return (
            self.db.execute(stmt)
            .unique()
            .scalars()
            .all()
        )

    def get_conversation(
        self,
        conversation_uuid: UUID,
    ):

        stmt = (
            select(Conversation)
            .options(
                joinedload(
                    Conversation.messages
                )
            )
            .where(
                Conversation.uuid == conversation_uuid,
                Conversation.tenant_id == self.tenant_id,
            )
        )

        return (
            self.db.execute(stmt)
            .unique()
            .scalar_one_or_none()
        )
    
    def get_open_conversation(
        self,
        customer_id: int,
    ):

        stmt = (
            select(Conversation)
            .where(
                Conversation.tenant_id == self.tenant_id,
                Conversation.customer_id == customer_id,
                Conversation.status == "Open",
            )
            .order_by(
                Conversation.created_at.desc()
            )
        )

        return self.db.scalar(stmt)

    def create_conversation(
        self,
        conversation: Conversation,
    ):

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def update_conversation(
        self,
        conversation: Conversation,
    ):

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    # =========================================================
    # MESSAGES
    # =========================================================

    def add_message(
        self,
        message: Message,
    ):

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_messages(
        self,
        conversation_id: int,
    ):

        stmt = (
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                Message.created_at.asc()
            )
        )

        return self.db.scalars(stmt).all()

    # =========================================================
    # EMAIL LOGS
    # =========================================================

    def get_email_logs(self):

        stmt = (
            select(EmailLog)
            .where(
                EmailLog.tenant_id == self.tenant_id
            )
            .order_by(
                EmailLog.created_at.desc()
            )
        )

        return self.db.scalars(stmt).all()

    def get_email_log(
        self,
        log_uuid: UUID,
    ):

        stmt = (
            select(EmailLog)
            .where(
                EmailLog.uuid == log_uuid,
                EmailLog.tenant_id == self.tenant_id,
            )
        )

        return self.db.scalar(stmt)

    def create_email_log(
        self,
        log: EmailLog,
    ):

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    def update_email_log(
        self,
        log: EmailLog,
    ):

        self.db.commit()
        self.db.refresh(log)

        return log

    def delete_email_log(
        self,
        log: EmailLog,
    ):

        self.db.delete(log)
        self.db.commit()

        # =========================================================
    # DASHBOARD
    # =========================================================

    def dashboard(self):

        total_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id
            )
        ) or 0

        total_customers = self.db.scalar(
            select(func.count(Customer.id)).where(
                Customer.tenant_id == self.tenant_id
            )
        ) or 0

        total_products = self.db.scalar(
            select(func.count(Product.id)).where(
                Product.tenant_id == self.tenant_id
            )
        ) or 0

        total_tickets = self.db.scalar(
            select(func.count(Ticket.id)).where(
                Ticket.tenant_id == self.tenant_id
            )
        ) or 0

        total_conversations = self.db.scalar(
            select(func.count(Conversation.id)).where(
                Conversation.tenant_id == self.tenant_id
            )
        ) or 0

        total_email_logs = self.db.scalar(
            select(func.count(EmailLog.id)).where(
                EmailLog.tenant_id == self.tenant_id
            )
        ) or 0

        pending_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id,
                Order.status == "Pending",
            )
        ) or 0

        delivered_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id,
                Order.status == "Delivered",
            )
        ) or 0

        cancelled_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id,
                Order.status == "Cancelled",
            )
        ) or 0

        returned_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id,
                Order.status == "Returned",
            )
        ) or 0

        refunded_orders = self.db.scalar(
            select(func.count(Order.id)).where(
                Order.tenant_id == self.tenant_id,
                Order.status == "Refunded",
            )
        ) or 0

        open_tickets = self.db.scalar(
            select(func.count(Ticket.id)).where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.status == "Open",
            )
        ) or 0

        resolved_tickets = self.db.scalar(
            select(func.count(Ticket.id)).where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.status == "Resolved",
            )
        ) or 0

        total_revenue = self.db.scalar(
            select(func.coalesce(func.sum(Order.total), 0)).where(
                Order.tenant_id == self.tenant_id,
                Order.payment_status == "Paid",
            )
        ) or 0

        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "delivered_orders": delivered_orders,
            "cancelled_orders": cancelled_orders,
            "returned_orders": returned_orders,
            "refunded_orders": refunded_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "resolved_tickets": resolved_tickets,
            "total_conversations": total_conversations,
            "emails_sent": total_email_logs,
            "total_revenue": float(total_revenue),
        }

    # =========================================================
    # ORDER ACTIONS
    # =========================================================

    def update_tracking(
        self,
        order: Order,
        courier: str,
        tracking_number: str,
    ):

        order.courier = courier
        order.tracking_number = tracking_number
        order.status = "Shipped"

        self.db.commit()
        self.db.refresh(order)

        return order

    def cancel_order(
        self,
        order: Order,
    ):

        order.status = "Cancelled"

        self.db.commit()
        self.db.refresh(order)

        return order

    def return_order(
        self,
        order: Order,
    ):

        order.status = "Returned"

        self.db.commit()
        self.db.refresh(order)

        return order

    def replace_order(
        self,
        order: Order,
    ):

        order.status = "Replacement Initiated"

        self.db.commit()
        self.db.refresh(order)

        return order

    def refund_order(
        self,
        order: Order,
    ):

        order.status = "Refunded"
        order.payment_status = "Refunded"

        self.db.commit()
        self.db.refresh(order)

        return order

    # =========================================================
    # SEARCH HELPERS
    # =========================================================

    def search_orders(
        self,
        keyword: str,
    ):

        stmt = (
            select(Order)
            .options(
                joinedload(Order.customer)
            )
            .where(
                Order.tenant_id == self.tenant_id,
                (
                    Order.order_number.ilike(f"%{keyword}%")
                )
            )
        )

        return (
            self.db.execute(stmt)
            .unique()
            .scalars()
            .all()
        )

    def search_customers(
        self,
        keyword: str,
    ):

        stmt = (
            select(Customer)
            .where(
                Customer.tenant_id == self.tenant_id,
                (
                    Customer.first_name.ilike(f"%{keyword}%")
                    |
                    Customer.last_name.ilike(f"%{keyword}%")
                    |
                    Customer.email.ilike(f"%{keyword}%")
                )
            )
        )

        return self.db.scalars(stmt).all()

    # =========================================================
    # UTILITIES
    # =========================================================

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def flush(self):
        self.db.flush()

    def refresh(self, instance):
        self.db.refresh(instance)
    