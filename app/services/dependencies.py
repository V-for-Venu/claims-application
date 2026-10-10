from typing import Annotated

from core.security import oauth2_scheme
from database.claim_sql_model import Provider
from database.session import get_db_session
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils import token_decoder

from services.claim_helper import ClaimService
from services.provider_helper import ProviderService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_claim_service(session: AsyncSessionDep):
    return ClaimService(session)


def get_provider_service(session: AsyncSessionDep):
    return ProviderService(session)


def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:

    decoded_token = token_decoder(token)
    if decoded_token is None:
        raise HTTPException(
            detail="Invalid Token, Please Provide valid Token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return decoded_token


async def get_current_provider(
    token_data: Annotated[dict, Depends(get_access_token)], service: AsyncSessionDep
):

    return await service.get(Provider, token_data["user"]["id"])


ServiceSessionDep = Annotated[ClaimService, Depends(get_claim_service)]

ProviderServiceDep = Annotated[ProviderService, Depends(get_provider_service)]

ProviderTokenDep = Annotated[Provider, Depends(get_current_provider)]
