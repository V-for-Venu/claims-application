import pytest
from httpx import AsyncClient

from .mock_data.mock_claims import MOCK_CLAIMS


def claim_payload(name: str = "Test Claim") -> dict:
    return {
        "ClaimName": name,
        "ClaimAmount": 125.50,
        "ClaimTPA": "Test TPA",
        "ClaimTin": "TIN-CLAIM-001",
        "ClaimPlaceOfService": "Chirala",
    }


@pytest.mark.asyncio
async def test_get_existing_claim(client: AsyncClient):
    claim_id = MOCK_CLAIMS[0]["ClaimId"]
    response = await client.get(f"/get/claims?id={claim_id}")

    assert response.status_code == 200
    assert response.json()["ClaimId"] == claim_id
    assert response.json()["ClaimName"] == "Xray Hand"
    assert response.json()["ClaimAmount"] == 80.6
    assert response.json()["ClaimTPA"] == "CNC"
    assert response.json()["Provider"]["ProviderMail"] == "vijayalabs@gmail.com"


@pytest.mark.asyncio
async def test_get_claim_not_found(client: AsyncClient):
    response = await client.get(
        "/get/claims?id=a4f1d268-d04b-4e17-b93e-2dc9d21d739e"
    )
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "Entity not found in the Database"


@pytest.mark.asyncio
async def test_get_claim_rejects_invalid_uuid(client: AsyncClient):
    response = await client.get("/get/claims?id=not-a-uuid")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_claim_lifecycle(client: AsyncClient, provider_token: str):
    headers = {"Authorization": f"Bearer {provider_token}"}
    create_response = await client.post(
        "/add/claims", json=claim_payload(), headers=headers
    )

    assert create_response.status_code == 200
    assert "Claim Created Successfully" in create_response.json()["message"]
    claim_id = create_response.json()["message"].rsplit(" ", 1)[-1]

    get_response = await client.get(f"/get/claims?id={claim_id}")
    assert get_response.status_code == 200
    assert get_response.json()["ClaimName"] == "Test Claim"
    assert get_response.json()["ClaimStatus"] == "Initiated"

    update_response = await client.patch(
        f"/update/claims?id={claim_id}",
        json={"ClaimStatus": "Approved"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Claim Updated Successfully"
    assert update_response.json()["updates"]["ClaimStatus"] == "Approved"

    updated_claim = await client.get(f"/get/claims?id={claim_id}")
    assert updated_claim.status_code == 200
    assert updated_claim.json()["ClaimStatus"] == "Approved"

    delete_response = await client.delete(
        f"/delete/claims?id={claim_id}", headers=headers
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Claim Deleted Successfully"

    deleted_claim = await client.get(f"/get/claims?id={claim_id}")
    assert deleted_claim.status_code == 404


@pytest.mark.asyncio
async def test_add_claim_requires_authentication(client: AsyncClient):
    response = await client.post("/add/claims", json=claim_payload())
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_add_claim_rejects_invalid_token(client: AsyncClient):
    response = await client.post(
        "/add/claims",
        json=claim_payload(),
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert "Invalid Token" in response.json()["detail"]["message"]


@pytest.mark.asyncio
async def test_update_claim_requires_authentication(client: AsyncClient):
    response = await client.patch(
        f"/update/claims?id={MOCK_CLAIMS[0]['ClaimId']}",
        json={"ClaimStatus": "Approved"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_claim_requires_authentication(client: AsyncClient):
    response = await client.delete(f"/delete/claims?id={MOCK_CLAIMS[0]['ClaimId']}")
    assert response.status_code == 401

