from contextlib import asynccontextmanager

from claims_data import claims_data
from claims_data_model import AddClaimData, ClaimResponse, ClaimStatus
from database import Database
from fastapi import FastAPI, HTTPException, status
from new_database.claims_sql_data_model import Claims
from new_database.session import SessionDep, create_db_tables
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference
from utils import claim_exists

db = Database()


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("...Server Started...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("...Server Stopped...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)


@app.get("/get/claims")
async def get_claims(id: int, session: SessionDep):

    claim_data = session.get(Claims, id)
    if claim_data:
        return claim_data.model_dump()
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )

    # -- Static Data Code -- #
    # if claim_exists(id):
    #     return ClaimResponse(**{"ClaimId": id, **claims_data[id]})

    # ____ DB Access with Plain SQL Queries and Classes ____
    # result = db.get_claims(id)
    # if result:
    #     return ClaimResponse.from_claim_tuple(result)
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Claim ID not found. Please provide a valid claim ID."
    #     )


@app.post("/add/claims")
async def add_claims(claim_data: AddClaimData, session: SessionDep) -> dict:

    new_claim = Claims(
        **claim_data.model_dump(),
        ClaimStatus=ClaimStatus.Initiated.value,
    )
    try:
        session.add(new_claim)
        session.commit()
        return {"detail": f"Claim Created Succesfully with Id: {new_claim.ClaimId}"}
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            detail=f"Error while Adding Claim, refer to this Image {e}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # -- Static Data Code -- #

    # while (new_claim_id := random.randint(10000, 99999)) in claims_data:
    #     pass

    # try:
    #     claims_data[new_claim_id] = claim_data.model_dump()
    #     return {"message": f"Claim Addedd Successfully with ID: {new_claim_id}"}

    # ____ DB Access with Plain SQL Queries and Classes ____
    # try:
    #     result = db.add_claim(claim_data)
    #     if result:
    #         return {
    #             "message": f"Claim Created Successfully with ID: {result} "
    #         }
    #     else:
    #         return HTTPException(
    #             status_code= status.HTTP_404_NOT_FOUND,
    #             detail=f"Unable to create Claim, Refer to message {result}"
    #         )

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Invalid Claim Data.. Refer to below Error f{str(e)}"
    #     )


# ___ TESTING PUT - NOT REQUIRED ____
@app.put("/update/claims")
async def update_claims(id: int, new_claim_record: AddClaimData) -> dict:

    if claim_exists(id):
        try:
            claims_data[id] = new_claim_record.model_dump()
            return {"message": "Claim Record Updated Successfully"}
        except Exception as e:  # noqa: BLE001
            return {"message": f"Error while Updating Claim Record: {e}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim ID not found. Please provide a valid Claim ID.",
        )


@app.patch("/update/claims/status")
async def update_claim_status(id: int, claim_status: str, session: SessionDep) -> dict:

    claim_data = session.get(Claims, id)
    if claim_data:
        claim_data.ClaimStatus = claim_status
        session.commit()
        return {"detail": "Claim Updated Successfully"}

    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )

    # ____ DB Access with Plain SQL Queries and Classes ____

    # try:
    #     if status in ["Approved", "Rejected", "Pending"] and not db.update_claim(id, status):
    #         return {
    #             "message": "Claim Updated Successfully.."
    #         }
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Unable to Update Claim Status, Please Check Status - {e}"
    #     )

    # -- Static Data Code -- #

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
async def delete_claims(id: int, session: SessionDep) -> dict:

    claims_data = session.get(Claims, id)
    if claims_data:
        session.delete(claims_data)
        session.commit()
        return {"detail": "Claim Deleted Successfully.."}
    else:
        raise HTTPException(
            detail="Claim not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )

    session.delete(Claims, id)

    # ____ DB Access with Plain SQL Queries and Classes ____

    # result=db.delete_claim(id)
    # try:
    #     result = db.delete_claim(id)
    #     if not result:
    #         return {
    #             "message": "Claim Deleted Successfully"
    #         }
    # except Exception as e:
    #     return HTTPException(
    #         status_code= status.HTTP_404_NOT_FOUND,
    #         detail=f"Unable to Delete Claim, Refer to Status - {e}"

    #     )

    # -- Static Data Code -- #

    # if claim_exists(id):
    #     del claims_data[id]
    #     return {"message": f"Claim Record with ID: {id} Deleted Successfully"}
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail = "Claim ID not found. Please provide a valid Claim ID."
    #     )


@app.get("/get/claims/latest")
async def get_latest_claim(session: SessionDep) -> ClaimResponse:
    return ClaimResponse.from_claim_tuple(db.get_latest_claims())


# -- Static Data Code -- #

# latest_claim_id = max(
#     claims_data.keys(),
#     key=lambda k: claims_data[k]["ClaimDate"])
# return {"ClaimId": latest_claim_id, **claims_data[latest_claim_id]}


@app.get("/get/claims/total")
async def get_total_claims(session: SessionDep) -> dict:
    total_claims, total_claims_amount = db.get_total_claims()
    return {
        "Total Claims": total_claims,
        "Total Claims Amount": round(total_claims_amount, 3),
    }


@app.get("/get/all/claimIds")
async def get_all_claim_ids(session: SessionDep):
    result = db.get_all_claimIds()
    return {"claim_ids": [i[0] for i in result]}
