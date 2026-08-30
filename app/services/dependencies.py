from typing import Annotated

from database.session import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.claim_helper import ClaimService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_shipment_service(session: AsyncSessionDep):
    return ClaimService(session)


ServiceSessionDep = Annotated[ClaimService, Depends(get_shipment_service)]
