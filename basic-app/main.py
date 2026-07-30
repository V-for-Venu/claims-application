from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
import random
from claims_data_model import AddClaimData

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)


@app.get("/get/claims")
async def get_claims(id: int | None = None) -> dict:
    if id in claims_data:
        return claims_data[id]
    elif id is None:
        return claims_data[max(claims_data.keys())]
    else:
        return {
            "message": "Claim ID not found. Please provide a valid claim ID."
        }


@app.post("/add/claims")
async def add_claims(claim_data: AddClaimData) -> dict:
    while (new_claim_id := random.randint(10000, 99999)) in claims_data:
        pass
    if new_claim_id not in claims_data:
        claims_data[new_claim_id] = claim_data.model_dump()
        return {"message": f"Claim Addedd Successfully with ID: {new_claim_id}"}

    else:
        return {
            "ERROR": "Invalid Claim Data"
        }



claims_data = {
    12345: {
        "claim_name": "Full Body Checkup",
        "claim_amount": 1000.00,
        "claim_status": "Pending",
        "claim_date": "2023-10-01"
    },
    19203 : {
        "claim_name": "Dental Checkup",
        "claim_amount": 500.00,
        "claim_status": "Approved",
        "claim_date": "2023-09-15"
    },
    39121: {
        "claim_name": "Vision Test",
        "claim_amount": 300.00,
        "claim_status": "Rejected",
        "claim_date": "2023-08-20"
    },
    9231: {
        "claim_name": "Physical Therapy",
        "claim_amount": 800.00,
        "claim_status": "Pending",
        "claim_date": "2023-07-10"
    },
    12312: {
        "claim_name": "Chiropractic Adjustment",
        "claim_amount": 600.00,
        "claim_status": "Approved",
        "claim_date": "2023-06-05"
    }
}