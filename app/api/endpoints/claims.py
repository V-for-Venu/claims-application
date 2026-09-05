from fastapi import APIRouter, HTTPException, status
from schemas.claim_schema import (
    AddClaimData,
    ClaimResponse,
    UpdateClaim,
)
from services.dependencies import ServiceSessionDep

router = APIRouter(tags=["Claims"])


@router.get("/get/claims", response_model=ClaimResponse)
async def get_claims(id: int, service: ServiceSessionDep) -> ClaimResponse:

    claim_data = await service.get_claim(id)
    if claim_data:
        return claim_data.model_dump()
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )


@router.post("/add/claims")
async def add_claims(claim_data: AddClaimData, service: ServiceSessionDep) -> dict:

    try:
        new_claim = await service.create_claim(claim_data)
        return {"detail": f"Claim Created Succesfully with Id: {new_claim.ClaimId}"}
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            detail=f"Error while Adding Claim, refer to this Error: {e}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.patch("/update/claims")
async def update_claim_status(
    id: int, payload: UpdateClaim, service: ServiceSessionDep
) -> dict:

    update_claim = await service.update_claim(id=id, payload=payload)
    if update_claim:
        return {"detail": f"Claim {id} Updated Successfully"}
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )


@router.delete("/delete/claims")
async def delete_claims(id: int, service: ServiceSessionDep) -> dict:

    delete_claim = await service.delete_claim(id=id)
    if delete_claim:
        return {"detail": "Claim Deleted Successfully.."}
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )
