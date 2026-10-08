from datetime import datetime, timedelta, timezone

import jwt
from config import security_settings


def token_generator(
    provider_data: dict,
) -> str:
    token = jwt.encode(
        payload={
            **provider_data,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )

    return token


def token_decoder(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

    except jwt.DecodeError:
        return None
