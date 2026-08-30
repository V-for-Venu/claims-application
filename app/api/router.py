from database.claims_sql_data_model import Claims
from database.session import AsyncSessionDep
from fastapi import APIRouter, HTTPException, status

# from claims_data import claims_data - Old Claims Data - Not Required
from app.api.schemas.claim_schema import (
    AddClaimData,
    ClaimResponse,
    ClaimStatus,
    UpdateClaim,
)

router = APIRouter()


@router.get("/get/claims", response_model=ClaimResponse)
async def get_claims(id: int, session: AsyncSessionDep) -> ClaimResponse:

    claim_data = await session.get(Claims, id)
    if claim_data:
        return claim_data.model_dump()
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )


@router.post("/add/claims")
async def add_claims(claim_data: AddClaimData, session: AsyncSessionDep) -> dict:

    new_claim = Claims(
        **claim_data.model_dump(),
        ClaimStatus=ClaimStatus.Initiated.value,
    )
    try:
        session.add(new_claim)
        await session.commit()
        return {"detail": f"Claim Created Succesfully with Id: {new_claim.ClaimId}"}
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            detail=f"Error while Adding Claim, refer to this Image {e}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.patch("/update/claims")
async def update_claim_status(
    id: int, payload: UpdateClaim, session: AsyncSessionDep
) -> dict:

    claim_data = await session.get(Claims, id)
    if claim_data:
        claim_data.ClaimStatus = payload.ClaimStatus.value
        claim_data.ClaimAuditTime = payload.ClaimAuditTime
        await session.commit()
        return {"detail": f"Claim {id} Updated Successfully"}

    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )


@router.delete("/delete/claims")
async def delete_claims(id: int, session: AsyncSessionDep) -> dict:

    claims_data = await session.get(Claims, id)
    if claims_data:
        await session.delete(claims_data)
        await session.commit()
        return {"detail": "Claim Deleted Successfully.."}
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )
