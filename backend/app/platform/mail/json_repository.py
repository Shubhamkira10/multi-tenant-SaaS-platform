from __future__ import annotations

from uuid import UUID

from app.core.tenant_json import TenantJsonLoader


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
        return self.loader.customers()

    # =========================================================
    # PRODUCTS
    # =========================================================

    def get_products(self):
        return self.loader.products()

    # =========================================================
    # ORDERS
    # =========================================================

    def get_orders(self):
        return self.loader.orders()

    # =========================================================
    # TICKETS
    # =========================================================

    def get_tickets(self):
        return self.loader.tickets()

    # =========================================================
    # CONVERSATIONS
    # =========================================================

    def get_conversations(self):
        return self.loader.conversations()

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