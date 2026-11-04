from enum import Enum


class Tag(str, Enum):
    """Tags for API Endpoints."""

    CLAIMS = "Claims"
    PROVIDERS = "Providers"
