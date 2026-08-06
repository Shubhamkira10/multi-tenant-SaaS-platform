from __future__ import annotations

import json


def build_prompt(
    customer,
    order,
    product,
    ticket,
    conversation,
    request,
):

    return f"""
You are an AI Customer Support Executive for ELEMENTAL CONCEPT.

Customer

{json.dumps(customer, indent=4)}

Order

{json.dumps(order, indent=4)}

Product

{json.dumps(product, indent=4)}

Ticket

{json.dumps(ticket, indent=4)}

Previous Conversation

{json.dumps(conversation, indent=4)}

Customer Email

Subject:
{request.subject}

Body:
{request.body}

Return ONLY valid JSON.

{{
    "intent":"",
    "backend_action":"",
    "parameters":{{}},
    "subject":"",
    "reply":""
}}
"""