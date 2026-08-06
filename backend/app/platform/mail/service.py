from __future__ import annotations

from app.modules.email.processor import MailProcessor


class MailService:

    def __init__(self, repo):
        self.repo = repo

    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(self):
        return self.repo.dashboard()

    # =====================================================
    # CUSTOMERS
    # =====================================================

    def get_customers(self):
        return self.repo.get_customers()

    def create_customer(self, data):
        return self.repo.create_customer(data)

    def update_customer(self, customer_uuid, data):
        return self.repo.update_customer(
            customer_uuid,
            data,
        )

    def delete_customer(self, customer_uuid):
        return self.repo.delete_customer(
            customer_uuid,
        )

    # =====================================================
    # PRODUCTS
    # =====================================================

    def get_products(self):
        return self.repo.get_products()

    def create_product(self, data):
        return self.repo.create_product(data)

    def update_product(self, product_uuid, data):
        return self.repo.update_product(
            product_uuid,
            data,
        )

    def delete_product(self, product_uuid):
        return self.repo.delete_product(
            product_uuid,
        )

    # =====================================================
    # ORDERS
    # =====================================================

    def get_orders(self):
        return self.repo.get_orders()

    def get_order(self, order_uuid):
        return self.repo.get_order(order_uuid)

    def create_order(self, data):
        return self.repo.create_order(data)

    def update_order(self, order_uuid, data):
        return self.repo.update_order(
            order_uuid,
            data,
        )

    def delete_order(self, order_uuid):
        return self.repo.delete_order(
            order_uuid,
        )

    # =====================================================
    # ORDER ACTIONS
    # =====================================================

    def update_address(self, order_uuid, data):
        return self.repo.update_address(
            order_uuid,
            data,
        )

    def track_order(self, order_uuid, data):
        return self.repo.track_order(
            order_uuid,
            data,
        )

    def cancel_order(self, order_uuid, data):
        return self.repo.cancel_order(
            order_uuid,
            data,
        )

    def return_order(self, order_uuid, data):
        return self.repo.return_order(
            order_uuid,
            data,
        )

    def replacement_order(self, order_uuid, data):
        return self.repo.replacement_order(
            order_uuid,
            data,
        )

    def refund_order(self, order_uuid, data):
        return self.repo.refund_order(
            order_uuid,
            data,
        )

    def generate_invoice(self, order_uuid):
        return self.repo.generate_invoice(
            order_uuid,
        )

    # =====================================================
    # TICKETS
    # =====================================================

    def get_tickets(self):
        return self.repo.get_tickets()

    def create_ticket(self, data):
        return self.repo.create_ticket(data)

    def update_ticket(self, ticket_uuid, data):
        return self.repo.update_ticket(
            ticket_uuid,
            data,
        )

    # =====================================================
    # CONVERSATIONS
    # =====================================================

    def get_conversations(self):
        return self.repo.get_conversations()

    def create_conversation(self, data):
        return self.repo.create_conversation(data)

    def add_message(self, conversation_uuid, data):
        return self.repo.add_message(
            conversation_uuid,
            data,
        )

    # =====================================================
    # EMAIL LOGS
    # =====================================================

    def get_email_logs(self):
        return self.repo.get_email_logs()

    # =====================================================
    # HEALTH
    # =====================================================

    def ping(self):
        return {
            "status": "ok",
            "module": "mail",
        }

    # =====================================================
    # TEST EMAIL
    # =====================================================

    def process_test_email(self, request):

        processor = MailProcessor(self.repo)

        return processor.process_test_email(
            request,
        )