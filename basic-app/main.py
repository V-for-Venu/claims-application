from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
import random
from claims_data_model import AddClaimData, ClaimResponse
from utils import claim_exists
from claims_data import claims_data
from database import Database

db = Database()
app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)


@app.get("/get/claims")
async def get_claims(id: int | None = None) -> ClaimResponse:
    result = db.get_claims(id)

    # if claim_exists(id):
    #     return ClaimResponse(**{"ClaimId": id, **claims_data[id]})
    
    if result:
        return ClaimResponse.from_claim_tuple(result)    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim ID not found. Please provide a valid claim ID."
        )


@app.post("/add/claims")
async def add_claims(claim_data: AddClaimData) -> dict:

    # while (new_claim_id := random.randint(10000, 99999)) in claims_data:
    #     pass

    # try:
    #     claims_data[new_claim_id] = claim_data.model_dump()
    #     return {"message": f"Claim Addedd Successfully with ID: {new_claim_id}"}

    try:
        result = db.add_claim(claim_data)
        if result:
            return {
                "message": f"Claim Created Successfully with ID: {result} "
            }
        else:
            return HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"Unable to create Claim, Refer to message {result}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Claim Data.. Refer to below Error f{str(e)}"
        )


@app.put("/update/claims")
async def update_claims(id: int, new_claim_record: AddClaimData) -> dict:
    if claim_exists(id):
        try:
            claims_data[id] = new_claim_record.model_dump()
            return {"message" : "Claim Record Updated Successfully"}
        except Exception as e:
            return {"message": f"Error while Updating Claim Record: {str(e)}"}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Claim ID not found. Please provide a valid Claim ID."
        )


@app.patch("/update/claims/status")
async def update_claim_status(id: int, status: str) -> dict:

    try:
        if status in ["Approved", "Rejected", "Pending"] and not db.update_claim(id, status):
            return {
                "message": "Claim Updated Successfully.."
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to Update Claim Status, Please Check Status - {e}"
        )

    # if claim_exists(id):
    #     if status in ["Approved", "Rejected", "Pending"]:
    #         claims_data[id]["ClaimStatus"] = status
    #         return {"message": f"Claim Status Updated Successfully to {status}"}
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Invalid Claim Status. Please provide a valid status: Approved, Rejected, or Pending."
    #         )


@app.delete("/delete/claims")
async def delete_claims(id: int) -> dict:
    result=db.delete_claim(id)
    print(result)
    try:
        result = db.delete_claim(id)
        if not result:
            return {
                "message": "Claim Deleted Successfully"
            }
    except Exception as e:
        return HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Unable to Delete Claim, Refer to Status - {e}"

        )



    # if claim_exists(id):
    #     del claims_data[id]
    #     return {"message": f"Claim Record with ID: {id} Deleted Successfully"}
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail = "Claim ID not found. Please provide a valid Claim ID."
    #     )


@app.get("/get/claims/latest")
async def get_latest_claim() -> dict:
    latest_claim_id = max(
        claims_data.keys(), 
        key=lambda k: claims_data[k]["ClaimDate"])
    return {"ClaimId": latest_claim_id, **claims_data[latest_claim_id]}


@app.get("/get/claims/total")
async def get_total_claims() -> dict:
    return {
        "total_claims_count": len(claims_data)
    }


@app.get("/get/all/claimIds")
async def get_all_claim_ids():
    return {"claim_ids": list(claims_data.keys())}
