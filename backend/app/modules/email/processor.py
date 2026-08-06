from app.modules.email.gemini_client import GeminiClient
from app.modules.email.prompt_builder import build_prompt
from app.modules.email.brevo_client import BrevoClient
from app.modules.email.template import build_email_html
from app.modules.email.order_extractor import extract_order_id

class MailProcessor:

    def __init__(self, repo):
        self.repo = repo
        self.gemini = GeminiClient()
        self.brevo = BrevoClient()

    def process_test_email(self, request):

        # ---------------------------------------------------
        # Customer
        # ---------------------------------------------------

        customer = self.repo.get_customer_by_email(
            request.senderEmail,
        )

        # ---------------------------------------------------
        # Extract Order ID
        # ---------------------------------------------------

        order_id = extract_order_id(
            request.subject,
            request.body,
        )

        orders = self.repo.get_orders()

        order = None
        reason = None

        # ---------------------------------------------------
        # CASE 1
        # Customer mentioned an Order ID
        # ---------------------------------------------------

        if order_id:

            order = next(

                (
                    o
                    for o in orders
                    if o["order_id"].upper() == order_id.upper()
                ),

                None,

            )

            if order is None:
                reason = "invalid_order_id"

        # ---------------------------------------------------
        # CASE 2
        # No Order ID
        # ---------------------------------------------------

        else:

            if customer:

                order = next(

                    (
                        o
                        for o in orders
                        if o["customer_email"].lower()
                        == request.senderEmail.lower()
                    ),

                    None,

                )

            if order is None:
                reason = "no_order_id"

        # ---------------------------------------------------
        # Product
        # ---------------------------------------------------

        product = {}

        if order:

            product = next(

                (
                    p
                    for p in self.repo.get_products()
                    if p["product_id"] == order["product_id"]
                ),

                {},

            )

        # ---------------------------------------------------
        # Ticket
        # ---------------------------------------------------

        ticket = {}

        if order:

            ticket = next(

                (
                    t
                    for t in self.repo.get_tickets()
                    if t["order_id"] == order["order_id"]
                ),

                {},

            )

        # ---------------------------------------------------
        # Previous Conversation
        # ---------------------------------------------------

        previous = None

        if order:

            previous = next(

                (
                    c
                    for c in self.repo.get_conversations()
                    if c.get("order_id") == order["order_id"]
                ),

                None,

            )

        # ---------------------------------------------------
        # Build Prompt
        # ---------------------------------------------------

        prompt = build_prompt(

            customer,

            order,

            product,

            ticket,

            previous,

            request,

            reason,

        )

        # ---------------------------------------------------
        # Gemini
        # ---------------------------------------------------

        ai = self.gemini.generate(prompt)

        # ---------------------------------------------------
        # Email HTML
        # ---------------------------------------------------

        html = build_email_html(
            ai["reply"],
        )

        settings = self.repo.get_mail_settings()

        # ---------------------------------------------------
        # Send Email
        # ---------------------------------------------------

        message_id = self.brevo.send(

            sender_name=settings["sender_name"],

            sender_email=settings["support_email"],

            reply_to=settings["reply_to_email"],

            recipient=request.senderEmail,

            subject=ai["subject"],

            html=html,

        )

        # ---------------------------------------------------
        # Conversation
        # ---------------------------------------------------

        if previous:

            conversation = previous

        else:

            conversation = self.repo.create_conversation(

                customer=customer,
                order=order,
                subject=request.subject,

            )

        # ---------------------------------------------------
        # Incoming Message
        # ---------------------------------------------------

        self.repo.add_message(

            conversation["conversation_id"],

            "incoming",

            request.senderEmail,

            request.subject,

            request.body,

        )

        # ---------------------------------------------------
        # Outgoing Message
        # ---------------------------------------------------

        self.repo.add_message(

            conversation["conversation_id"],

            "outgoing",

            settings["sender_name"],

            ai["subject"],

            ai["reply"],

        )

        # ---------------------------------------------------
        # Email Log
        # ---------------------------------------------------

        self.repo.create_email_log(

            customer_email=customer["email"] if customer else request.senderEmail,

            customer_uuid=customer["uuid"] if customer else None,

            order_uuid=order["uuid"] if order else None,

            conversation_uuid=conversation["uuid"],

            message_id=message_id,

            backend_action=ai.get(
                "backend_action",
                "NONE",
            ),

            provider="Gemini",

            status="Processed",

        )

        # ---------------------------------------------------
        # Response
        # ---------------------------------------------------

        return {

            "success": True,

            "conversation_id": conversation["conversation_id"],

            "reply": ai["reply"],

            "intent": ai.get("intent"),

            "backend_action": ai.get("backend_action"),

        }