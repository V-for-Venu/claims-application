from uuid import uuid4

import jwt
from config import security_settings
from constants import token_expiry_time
from fastapi import HTTPException, status


def token_generator(
    provider_data: dict,
) -> str:
    token = jwt.encode(
        payload={
            **provider_data,
            "jti": str(uuid4()),
            "exp": token_expiry_time,
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

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            detail="Token Expired, Please Authenticate Again.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    except jwt.DecodeError:
        return None
