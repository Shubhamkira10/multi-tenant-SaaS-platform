from __future__ import annotations

from uuid import UUID
import uuid

from app.core.tenant_json import TenantJsonLoader
from datetime import datetime

class JsonMailRepository:

    def __init__(
        self,
        tenant_uuid: UUID,
    ):

        self.loader = TenantJsonLoader(
            tenant_uuid
        )

    # =========================================================
    # CUSTOMERS
    # =========================================================

    def get_customers(self):
        customers = self.loader.customers()
        orders = self.loader.orders()
        tickets = self.loader.tickets()

        enriched = []

        for customer in customers:

            customer_orders = [
                order
                for order in orders
                if order["customer_email"].lower() == customer["email"].lower()
            ]

            order_count = len(customer_orders)

            order_uuids = {
                order["uuid"]
                for order in customer_orders
            }

            ticket_count = sum(
                1
                for ticket in tickets
                if ticket.get("order_uuid") in order_uuids
            )

            enriched.append(
                {
                    **customer,
                    "order_count": order_count,
                    "ticket_count": ticket_count,
                }
            )

        return enriched

# =========================================================
# PRODUCTS
# =========================================================
    def get_products(self):
        products = self.loader.products()
        orders = self.loader.orders()

        result = []

        for product in products:
            product = product.copy()

            product["order_count"] = sum(
                1
                for order in orders
                if order["product_id"] == product["product_id"]
            )

            result.append(product)

        return result

    # =========================================================
    # ORDERS
    # =========================================================

    def get_orders(self):
        return self.loader.orders()

# =========================================================
# TICKETS
# =========================================================
    def get_tickets(self):
        tickets = self.loader.tickets()
        orders = self.loader.orders()

        result = []

        for ticket in tickets:
            ticket = ticket.copy()

            order = next(
                (
                    o for o in orders
                    if o["uuid"] == ticket["order_uuid"]
                ),
                None,
            )

            if order:
                ticket["order_id"] = order["order_id"]
                ticket["customer_name"] = order["customer_name"]
                ticket["customer_email"] = order["customer_email"]
            else:
                ticket["order_id"] = "-"
                ticket["customer_name"] = "Unknown"
                ticket["customer_email"] = ""

            result.append(ticket)

        return result

    # =========================================================
    # CONVERSATIONS
    # =========================================================
    def get_conversations(self):
        conversations = self.loader.conversations()
        orders = self.loader.orders()
        customers = self.loader.customers()

        order_map = {
            o["uuid"]: o
            for o in orders
        }

        customer_map = {
            c["uuid"]: c
            for c in customers
        }

        result = []

        for conv in conversations:

            order = order_map.get(conv.get("order_uuid"))
            customer = customer_map.get(conv.get("customer_uuid"))

            result.append({

                **conv,

                "order_id": order["order_id"] if order else None,

                "customer_name": customer["name"] if customer else "Unknown",

                "customer_email": customer["email"] if customer else "",

                "message_count": len(conv.get("messages", [])),

            })

        return result

    # =========================================================
    # EMAIL LOGS
    # =========================================================

    def get_email_logs(self):
        return self.loader.email_logs()

    # =========================================================
    # DASHBOARD
    # =========================================================

    def dashboard(self):

        customers = self.loader.customers()
        products = self.loader.products()
        orders = self.loader.orders()
        tickets = self.loader.tickets()
        conversations = self.loader.conversations()
        email_logs = self.loader.email_logs()

        return {

            "total_customers": len(customers),

            "total_products": len(products),

            "total_orders": len(orders),

            "total_tickets": len(tickets),

            "total_conversations": len(conversations),

            "emails_sent": len(email_logs),

        }

    def get_customer_by_email(self, email: str):
        customers = self.loader.customers()

        for customer in customers:
            if customer["email"].lower() == email.lower():
                return customer

        return None
    
    def create_conversation(
        self,
        customer,
        order,
        subject,
    ):
        conversations = self.loader.conversations()

        if order:
            conversation_id = f"CONV-{order['order_id']}"
            order_uuid = order["uuid"]
            order_id = order["order_id"]
        else:
            conversation_id = f"CONV-{uuid.uuid4().hex[:8].upper()}"
            order_uuid = None
            order_id = None

        conversation = {
            "uuid": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "customer_uuid": customer["uuid"] if customer else None,
            "customer_email": customer["email"] if customer else None,
            "customer_name": customer["name"] if customer else "Unknown",
            "order_uuid": order_uuid,
            "order_id": order_id,
            "subject": subject,
            "status": "OPEN",
            "created_at": datetime.utcnow().isoformat(),
            "messages": [],
        }

        conversations.append(conversation)

        self.loader.write(
            "conversations.json",
            conversations,
        )

        return conversation

    def add_message(
        self,
        conversation_id,
        direction,
        sender,
        subject,
        body,
    ):

        conversations = self.loader.conversations()

        for conversation in conversations:

            if conversation["conversation_id"] == conversation_id:

                conversation["messages"].append(

                    {

                        "message_id": str(uuid.uuid4()),

                        "direction": direction,

                        "channel": "Email",

                        "sender": sender,

                        "subject": subject,

                        "body": body,

                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                    }

                )

                self.loader.write(
                    "conversations.json",
                    conversations,
                )

                return

    def create_email_log(
        self,
        customer_email: str,
        customer_uuid: str,
        order_uuid: str,
        conversation_uuid: str,
        message_id: str,
        backend_action: str = "NONE",
        provider: str = "Gemini",
        status: str = "Processed",
    ):

        logs = self.loader.email_logs()

        logs.append(
            {
                "uuid": str(uuid.uuid4()),
                "message_id": message_id,
                "conversation_uuid": conversation_uuid,
                "customer_uuid": customer_uuid,
                "customer_email": customer_email,
                "order_uuid": order_uuid,
                "backend_action": backend_action,
                "processed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "provider": provider,
                "status": status,
            }
        )

        self.loader.write(
            "email_logs.json",
            logs,
        )
    
# =========================================================
# CUSTOMER CRUD
# =========================================================
    def create_customer(self, data):

        customers = self.loader.customers()

        customer = {
            "uuid": str(uuid.uuid4()),
            "customer_id": f"CUS{1000 + len(customers) + 1}",
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "total_orders": 0,
            "total_spent": 0,
            "created_at": datetime.utcnow().isoformat(),
        }

        customers.append(customer)

        self.loader.write(
            "customers.json",
            customers,
        )

        return customer


    def update_customer(
        self,
        customer_uuid,
        data,
    ):

        customers = self.loader.customers()

        for customer in customers:

            if customer["uuid"] == str(customer_uuid):

                values = data.model_dump(
                    exclude_unset=True,
                )

                customer.update(values)

                self.loader.write(
                    "customers.json",
                    customers,
                )

                return customer

        raise ValueError("Customer not found")


    def delete_customer(
        self,
        customer_uuid,
    ):

        customers = self.loader.customers()

        customers = [

            customer

            for customer in customers

            if customer["uuid"] != str(customer_uuid)

        ]

        self.loader.write(
            "customers.json",
            customers,
        )

        return True
    
    def get_mail_settings(self):

        return {

            "sender_name": "Elemental Concept",

            "support_email": "support@elementalconcept.com",

            "reply_to_email": "support@elementalconcept.com",

        }