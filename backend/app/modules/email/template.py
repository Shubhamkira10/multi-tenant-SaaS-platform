from __future__ import annotations


def build_email_html(reply: str):

    reply = reply.replace("\n", "<br>")

    return f"""
    <!DOCTYPE html>
    <html>

    <body style="font-family:Arial;padding:20px">

        <h2>ELEMENTAL CONCEPT</h2>

        <hr>

        <div>

            {reply}

        </div>

        <br>

        <hr>

        <small>
        This email was generated automatically by the
        ELEMENTAL CONCEPT AI Customer Support System.
        </small>

    </body>

    </html>
    """