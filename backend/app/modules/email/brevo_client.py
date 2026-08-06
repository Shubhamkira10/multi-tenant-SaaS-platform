from __future__ import annotations

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings

class BrevoClient:

    def __init__(self):

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        self.client = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

    def send(
        self,
        sender_name,
        sender_email,
        reply_to,
        recipient,
        subject,
        html,
    ):

        email = sib_api_v3_sdk.SendSmtpEmail(

            sender={
                "name": sender_name,
                "email": sender_email,
            },

            to=[
                {
                    "email": recipient,
                }
            ],

            reply_to={
                "email": reply_to,
            },

            subject=subject,

            html_content=html,
        )

        try:

            response = self.client.send_transac_email(
                email
            )

            return response.message_id

        except ApiException as e:

            raise RuntimeError(str(e))