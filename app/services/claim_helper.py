from core.exceptions import AuthorizationError, EntityNotFoundError, InvalidRequestError
from database.claim_sql_model import Claims
from schemas.claim_schema import (
    AddClaimData,
    ClaimResponse,
    ClaimStatus,
    UpdateClaim,
)
from sqlalchemy.ext.asyncio import AsyncSession


class ClaimService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_claim(self, id) -> ClaimResponse:
        claim_data = await self.session.get(Claims, id)
        if not claim_data:
            raise EntityNotFoundError
        return claim_data

    async def create_claim(self, claim_data: AddClaimData, service) -> Claims:

        new_claim = Claims(
            **claim_data.model_dump(),
            ClaimStatus=ClaimStatus.Initiated.value,
            ClaimProviderId=service.ProviderId,
        )
        if not new_claim:
            raise InvalidRequestError

        self.session.add(new_claim)
        await self.session.commit()
        await self.session.refresh(new_claim)

        return new_claim.ClaimId

    async def update_claim(self, id, payload: UpdateClaim, providerService):
        claim_data = await self.get_claim(id)
        if not claim_data:
            raise EntityNotFoundError
        if claim_data.ClaimProviderId != providerService.ProviderId:
            raise AuthorizationError
        claim_data.ClaimStatus = payload.ClaimStatus.value
        claim_data.ClaimAuditTime = payload.ClaimAuditTime
        await self.session.commit()
        await self.session.refresh(claim_data)

        return {
            "ClaimId": claim_data.ClaimId,
            "ClaimStatus": claim_data.ClaimStatus,
            "ClaimAuditTime": claim_data.ClaimAuditTime,
        }

    async def delete_claim(self, id, providerService):
        claim_data = await self.get_claim(id)
        if not claim_data:
            raise EntityNotFoundError
        if claim_data.ClaimProviderId != providerService.ProviderId:
            raise AuthorizationError
        await self.session.delete(claim_data)
        await self.session.commit()
        return True
