from app.modules.email.gemini_client import GeminiClient
from app.modules.email.prompt_builder import build_prompt
from app.modules.email.brevo_client import BrevoClient
from app.modules.email.template import build_email_html


class MailProcessor:

    def __init__(self, repo):
        self.repo = repo
        self.gemini = GeminiClient()
        self.brevo = BrevoClient()

    def process_test_email(self, request):

        customer = self.repo.get_customer_by_email(
            request.senderEmail,
        )

        if customer is None:
            raise ValueError("Customer not found.")

        orders = self.repo.get_orders()

        order = next(
            (
                x
                for x in orders
                if x["customer_email"].lower()
                == request.senderEmail.lower()
            ),
            None,
        )

        if order is None:
            raise ValueError("Order not found.")

        product = next(
            (
                x
                for x in self.repo.get_products()
                if x["uuid"] == order["product_uuid"]
            ),
            {},
        )

        ticket = next(
            (
                x
                for x in self.repo.get_tickets()
                if x.get("order_uuid") == order.get("uuid")
            ),
            {},
        )

        previous = next(
            (
                x
                for x in self.repo.get_conversations()
                if x["order_uuid"] == order["uuid"]
            ),
            None,
        )

        prompt = build_prompt(
            customer,
            order,
            product,
            ticket,
            previous,
            request,
        )

        ai = self.gemini.generate(prompt)

        html = build_email_html(ai["reply"])

        settings = self.repo.get_mail_settings()

        message_id = self.brevo.send(
            sender_name=settings["sender_name"],
            sender_email=settings["support_email"],
            reply_to=settings["reply_to_email"],
            recipient=request.senderEmail,
            subject=ai["subject"],
            html=html,
        )

        if previous is None:
            conversation = self.repo.create_conversation(
                customer=customer,
                order=order,
                subject=request.subject,
            )
        else:
            conversation = previous

        self.repo.add_message(
            conversation["conversation_id"],
            "incoming",
            request.senderEmail,
            request.subject,
            request.body,
        )

        self.repo.add_message(
            conversation["conversation_id"],
            "outgoing",
            settings["sender_name"],
            ai["subject"],
            ai["reply"],
        )

        self.repo.create_email_log(
            customer_email=customer["email"],
            customer_uuid=customer["uuid"],
            order_uuid=order["uuid"],
            conversation_uuid=conversation["uuid"],
            message_id=message_id,
            backend_action=ai.get("backend_action", "NONE"),
            provider="Gemini",
            status="Processed",
        )

        return {
            "success": True,
            "conversation_id": conversation["conversation_id"],
            "reply": ai["reply"],
        }