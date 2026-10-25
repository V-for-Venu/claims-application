from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from config import security_settings
from constants import expiry_in_seconds
from core.exceptions import ExpiredTokenError, InvalidTokenError
from database.redis import check_jti_in_blacklist


def token_generator(
    provider_data: dict,
) -> str:
    token = jwt.encode(
        payload={
            **provider_data,
            "jti": str(uuid4()),
            "exp": datetime.now(tz=UTC) + timedelta(seconds=expiry_in_seconds),
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )

    return token


async def token_decoder(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
        if await check_jti_in_blacklist(decoded_token["jti"]):
            raise ExpiredTokenError

        return decoded_token

    except jwt.DecodeError:
        raise InvalidTokenError

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError


def unix_timestamp_converter(time: int):
    return datetime.fromtimestamp(time).strftime("%d %b %Y, %I:%M:%S %p")
