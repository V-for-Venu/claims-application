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
        return await self.session.get(Claims, id)

    async def create_claim(self, claim_data: AddClaimData) -> Claims:
        new_claim = Claims(
            **claim_data.model_dump(),
            ClaimStatus=ClaimStatus.Initiated.value,
        )
        self.session.add(new_claim)
        await self.session.commit()
        await self.session.refresh(new_claim)

        return new_claim

    async def update_claim(self, payload: UpdateClaim, id: int):
        claim_data = await self.get_claim(id)
        if claim_data:
            claim_data.ClaimStatus = payload.ClaimStatus.value
            claim_data.ClaimAuditTime = payload.ClaimAuditTime
            await self.session.commit()
            await self.session.refresh(claim_data)
            return True
        else:
            return None

    async def delete_claim(self, id: int):
        claim_data = await self.get_claim(id)
        if claim_data:
            await self.session.delete(claim_data)
            await self.session.commit()
            return True
        else:
            return None
