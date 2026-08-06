import re

ORDER_PATTERN = re.compile(r"\bORD\d+\b", re.IGNORECASE)


def extract_order_id(subject: str, body: str):
    text = f"{subject}\n{body}"

    match = ORDER_PATTERN.search(text)

    if match:
        return match.group().upper()

    return None