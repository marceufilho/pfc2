"""Content identities for reconstructed sources, drivers and datasets; never proof authority."""

import hashlib


def sha256_text(text: str) -> str:
    """Hex SHA-256 of UTF-8 text. Equal digests identify equal inputs, not verified ones."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
