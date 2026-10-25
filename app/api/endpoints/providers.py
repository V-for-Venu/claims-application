from typing import Annotated
from uuid import UUID

from constants import expiry_in_seconds
from core.security import oauth2_scheme
from database.redis import add_jti_to_blacklist, check_jti_in_blacklist
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.provider_schema import GetProvider, RegisterProvider
from services.dependencies import ProviderServiceDep, get_access_token
from utils import token_decoder, unix_timestamp_converter

router = APIRouter(prefix="/provider", tags=["Provider"])


@router.post("/signup")
async def register_provider(
    provider_data: RegisterProvider, service: ProviderServiceDep
) -> dict:
    try:
        new_provider = await service.create_provider(provider_data)
        return {
            "detail": f"Provider Created Succesfully with Id: {new_provider.ProviderId}"
        }
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            detail=f"Error while Adding Provider, refer to this Error: {e}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/get_provider")
async def get_provider(id: UUID, service: ProviderServiceDep) -> GetProvider:
    provider_data = await service.get_provider(id)
    if provider_data:
        return provider_data.model_dump()
    else:
        raise HTTPException(
            detail="Provider not found in DB...", status_code=status.HTTP_404_NOT_FOUND
        )


@router.post("/authentication")
async def login_provider(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ProviderServiceDep,
):
    token = await service.authenticate_provider(
        request_form.username, request_form.password
    )
    if not token:
        raise HTTPException(
            detail="Invalid Username or Password. Please try again.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return {
        "access_token": token,
        "token_type": "JWT",
        "exp_time": expiry_in_seconds,
    }


@router.get("/logout")
async def logout_provider(token_data: Annotated[dict, Depends(get_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"message": "Provider Logged Out Successfully"}


@router.get("/token/verify")
async def authorize_provider_token(
    token: Annotated[str, Depends(oauth2_scheme)], service: ProviderServiceDep
) -> dict:

    decoded_token = token_decoder(token)
    print(decoded_token)

    if decoded_token is None:
        raise HTTPException(
            detail="Invalid Token, Please Provide valid Token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if await check_jti_in_blacklist(decoded_token["jti"]):
        raise HTTPException(
            detail="Token Expired, Please Provide valid Token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    provider_data = await service.get_provider(decoded_token["user"]["id"])

    return {
        "message": "User Authorized Successfully..!!",
        "Provider_Details": provider_data.model_dump(exclude={"ProviderPassword"}),
        "expiry": unix_timestamp_converter(decoded_token["exp"]),
    }
