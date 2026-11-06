from typing import Annotated
from uuid import UUID

from constants import expiry_in_seconds
from core.security import oauth2_scheme
from database.redis import add_jti_to_blacklist
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.provider_schema import GetProvider, RegisterProvider
from services.dependencies import ProviderServiceDep, get_access_token
from utils import token_decoder, unix_timestamp_converter

router = APIRouter(prefix="/provider", tags=["Providers"])


@router.get(
    "/get_provider",
    name="Read Provider",
    description="Read Provider by **Provider ID**",
)
async def get_provider(id: UUID, service: ProviderServiceDep) -> GetProvider:
    return await service.get_provider(id)


@router.post(
    "/signup",
    name="Register Provider",
    description="Register a new Provider",
)
async def register_provider(
    provider_data: RegisterProvider, service: ProviderServiceDep
) -> dict:

    new_provider = await service.create_provider(provider_data)
    return {
        "detail": f"Provider Created Succesfully with Id: {new_provider.ProviderId}"
    }


@router.post(
    "/authentication",
    name="Login Provider",
    description="Login to the Provider Account",
)
async def login_provider(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ProviderServiceDep,
):
    token = await service.authenticate_provider(
        request_form.username, request_form.password
    )
    return {
        "access_token": token,
        "token_type": "JWT",
        "exp_time": expiry_in_seconds,
    }


@router.get(
    "/logout",
    name="Logout Provider",
    description="Logout of the Provider Account",
)
async def logout_provider(token_data: Annotated[dict, Depends(get_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"message": "Provider Logged Out Successfully"}


@router.get(
    "/token/verify",
    name="Verify Provider Token",
    description="Verify the validity of the Provider Token",
)
async def authorize_provider_token(
    token: Annotated[str, Depends(oauth2_scheme)], service: ProviderServiceDep
) -> dict:

    decoded_token = await token_decoder(token)

    provider_data = await service.get_provider(decoded_token["user"]["id"])

    return {
        "message": "User Authorized Successfully..!!",
        "Provider_Details": provider_data.model_dump(exclude={"ProviderPassword"}),
        "expiry": unix_timestamp_converter(decoded_token["exp"]),
    }
