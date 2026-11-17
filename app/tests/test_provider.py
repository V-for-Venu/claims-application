import pytest
from httpx import AsyncClient

from .mock_data.mock_claims import MOCK_PROVIDERS


@pytest.mark.asyncio
async def test_get_existing_provider(client: AsyncClient):
    provider_id = MOCK_PROVIDERS[0]["ProviderId"]
    response = await client.get(f"/provider/get_provider?id={provider_id}")

    assert response.status_code == 200
    assert response.json() == {
        "ProviderId": provider_id,
        "ProviderName": "Vijaya Labs",
        "ProviderMail": "vijayalabs@gmail.com",
        "ProviderType": "Hospital",
        "TIN": "12345678",
    }


@pytest.mark.asyncio
async def test_get_provider_not_found(client: AsyncClient):
    response = await client.get(
        "/provider/get_provider?id=ab12dd95-5cf5-4e4c-943e-ea98bbbc0fcf"
    )
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "Entity not found in the Database"


@pytest.mark.asyncio
async def test_get_provider_rejects_invalid_uuid(client: AsyncClient):
    response = await client.get("/provider/get_provider?id=not-a-uuid")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_provider(client: AsyncClient):
    provider_data = {
        "ProviderName": "Test Clinic",
        "ProviderMail": "new.provider@example.com",
        "ProviderPassword": "StrongTestPassword123!",
        "ProviderType": "Clinic",
        "TIN": "TIN-TEST-001",
    }
    response = await client.post("/provider/signup", json=provider_data)

    assert response.status_code == 200
    assert "Provider Created Succesfully with Id:" in response.json()["detail"]

    provider_id = response.json()["detail"].rsplit(" ", 1)[-1]
    get_response = await client.get(f"/provider/get_provider?id={provider_id}")
    assert get_response.status_code == 200
    assert get_response.json()["ProviderMail"] == provider_data["ProviderMail"]
    assert "ProviderPassword" not in get_response.json()


@pytest.mark.asyncio
async def test_register_provider_validation_error(client: AsyncClient):
    response = await client.post(
        "/provider/signup",
        json={
            "ProviderName": "Invalid Provider",
            "ProviderMail": "not-an-email",
            "ProviderPassword": "password",
            "ProviderType": "Unknown",
            "TIN": "TIN-TEST-002",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_provider_login_success(client: AsyncClient):
    response = await client.post(
        "/provider/authentication",
        data={"username": "vijayalabs@gmail.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "JWT"
    assert response.json()["access_token"]
    assert response.json()["exp_time"] == 1800


@pytest.mark.asyncio
async def test_provider_login_invalid_password(client: AsyncClient):
    response = await client.post(
        "/provider/authentication",
        data={"username": "vijayalabs@gmail.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["message"] == (
        "Invalid Credentials, Please provider Valid Credentials"
    )


@pytest.mark.asyncio
async def test_verify_provider_token(client: AsyncClient, provider_token: str):
    response = await client.get(
        "/provider/token/verify",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User Authorized Successfully..!!"
    assert response.json()["Provider_Details"]["ProviderMail"] == (
        "vijayalabs@gmail.com"
    )


@pytest.mark.asyncio
async def test_verify_provider_token_requires_authentication(client: AsyncClient):
    response = await client.get("/provider/token/verify")
    assert response.status_code == 401
