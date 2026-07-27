from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def generate_unique_slug(
    text: str,
    slug_exists: Callable[[str], bool],
) -> str:
    """
    Generate a unique slug.

    Example:
        elemental
        elemental-1
        elemental-2
        elemental-3
    """
    base_slug = slugify(text)
    slug = base_slug
    counter = 1

    while slug_exists(slug):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug