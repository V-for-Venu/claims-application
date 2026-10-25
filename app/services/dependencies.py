from typing import Annotated
from uuid import UUID

from core.security import oauth2_scheme
from database.claim_sql_model import Provider
from database.session import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import token_decoder

from services.claim_helper import ClaimService
from services.provider_helper import ProviderService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_claim_service(session: AsyncSessionDep):
    return ClaimService(session)


def get_provider_service(session: AsyncSessionDep):
    return ProviderService(session)


async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:

    return await token_decoder(token)


async def get_current_provider(
    token_data: Annotated[dict, Depends(get_access_token)], service: AsyncSessionDep
):

    return await service.get(Provider, UUID(token_data["user"]["id"]))


ServiceSessionDep = Annotated[ClaimService, Depends(get_claim_service)]

ProviderServiceDep = Annotated[ProviderService, Depends(get_provider_service)]

ProviderTokenDep = Annotated[Provider, Depends(get_current_provider)]
