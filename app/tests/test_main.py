import pytest
from httpx import AsyncClient
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty

from .mock_data.mock_claims import (
    MOCK_ADD_CLAIM,
    MOCK_CLAIMS,
    MOCK_PROVIDERS,
)


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    print("✅ Health check passed!")


@pytest.mark.asyncio
async def test_scalar(client: AsyncClient):
    response = await client.get("/scalar")
    assert response.status_code == 200
    assert "Scalar API Reference" in response.text
    print("✅ Scalar API reference check passed!")


@pytest.mark.asyncio
async def test_root(client: AsyncClient, test_id: str):
    response = await client.get("/")

    print(Panel(Pretty(response.json())))

    assert response.json() == {"detail": f"{test_id}"}
    assert response.status_code == 200
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_non_existent_claim(client: AsyncClient):
    response = await client.get("/get/claims?id=a4f1d268-d04b-4e17-b93e-2dc9d21d739e")

    print(Panel(Pretty(response.json())))

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "Entity not found in the Database"


@pytest.mark.asyncio
async def test_existing_claim(client: AsyncClient):
    claim_id = MOCK_CLAIMS[0]["ClaimId"]

    response = await client.get(f"/get/claims?id={claim_id}")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["ClaimName"] == "Xray Hand"
    assert response_data["ClaimAmount"] == 80.6
    assert response_data["ClaimTPA"] == "CNC"


@pytest.mark.asyncio
async def test_non_existent_provider(client: AsyncClient):

    response = await client.get(
        "/provider/get_provider?id=ab12dd95-5cf5-4e4c-943e-ea98bbbc0fcf"
    )

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "Entity not found in the Database"


@pytest.mark.asyncio
async def test_existing_provider(client: AsyncClient):
    provider_id = MOCK_PROVIDERS[0]["ProviderId"]

    response = await client.get(f"/provider/get_provider?id={provider_id}")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["ProviderName"] == "Vijaya Labs"
    assert response_data["ProviderMail"] == "vijayalabs@gmail.com"
    assert response_data["ProviderType"] == "Hospital"


async def test_valid_provider_login(client: AsyncClient):
    response = await client.post(
        "/provider/authentication",
        data={"username": "vijayalabs@gmail.com", "password": "password123"},
    )

    print(Panel(Pretty(response.json())))
    assert response.status_code == 200
    assert response.json()["token_type"] == "JWT"
    assert response.json()["access_token"] is not None
    assert response.json()["exp_time"] == 1800


async def test_invalid_provider_login(client: AsyncClient):
    response = await client.post(
        "/provider/authentication",
        data={"username": "vijayalabs@gmail.com", "password": "wrongpassword"},
    )

    print(Panel(Pretty(response.json())))
    assert response.status_code == 401
    assert (
        response.json()["detail"]["message"]
        == "Invalid Credentials, Please provider Valid Credentials"
    )


async def test_add_claim_authorized(client: AsyncClient, provider_token: str):
    response = await client.post(
        "/add/claims",
        json=MOCK_ADD_CLAIM[0],
        headers={"Authorization": f"Bearer {provider_token}"},
    )

    print(Panel(Pretty(response.json())))

    assert response.status_code == 200
    assert "Claim Created Successfully" in response.json()["message"]


async def test_add_claim_invalid_token(client: AsyncClient):
    response = await client.post(
        "/add/claims",
        json=MOCK_ADD_CLAIM[0],
        headers={"Authorization": "Bearer invalid_token"},
    )

    print(Panel(Pretty(response.json())))

    assert response.status_code == 401
    assert "Invalid Token" in response.json()["detail"]["message"]


async def test_add_claim_not_authenticated(client: AsyncClient):
    response = await client.post(
        "/add/claims",
        json=MOCK_ADD_CLAIM[0],
    )

    print(Panel(Pretty(response.json())))

    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]
