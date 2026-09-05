from typing import Annotated

from database.session import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.claim_helper import ClaimService
from services.provider_helper import ProviderService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_claim_service(session: AsyncSessionDep):
    return ClaimService(session)


def get_provider_service(session: AsyncSessionDep):
    return ProviderService(session)


ServiceSessionDep = Annotated[ClaimService, Depends(get_claim_service)]

ProviderServiceDep = Annotated[ProviderService, Depends(get_provider_service)]
