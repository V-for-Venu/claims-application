from uuid import UUID

from fastapi import APIRouter
from schemas.claim_schema import (
    AddClaimData,
    ClaimResponse,
    UpdateClaim,
)
from services.dependencies import ProviderTokenDep, ServiceSessionDep

router = APIRouter(tags=["Claims"])


@router.get("/get/claims", response_model=ClaimResponse)
async def get_claims(id: UUID, service: ServiceSessionDep) -> ClaimResponse:

    return await service.get_claim(id)


@router.post("/add/claims")
async def add_claims(
    claim_data: AddClaimData,
    service: ServiceSessionDep,
    providerService: ProviderTokenDep,
) -> dict:

    new_claim_id = await service.create_claim(claim_data, providerService)
    return {"message": f"Claim Created Successfully with ID f{new_claim_id}"}


@router.patch("/update/claims")
async def update_claim_status(
    id: UUID,
    payload: UpdateClaim,
    service: ServiceSessionDep,
    providerService: ProviderTokenDep,
) -> dict:

    updated_claim = await service.update_claim(id=id, payload=payload)
    return {"message": "Claim Updated Successfully", "updates": updated_claim}


@router.delete("/delete/claims")
async def delete_claims(
    id: UUID,
    service: ServiceSessionDep,
    providerService: ProviderTokenDep,
) -> dict:

    if await service.delete_claim(id=id):
        return {"message": "Claim Deleted Successfully", "deleted_claim": id}
