from typing import Annotated

from constants import expiry_in_seconds
from core.security import oauth2_scheme
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.provider_schema import GetProvider, RegisterProvider
from services.dependencies import ProviderServiceDep, get_access_token
from utils import token_decoder

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
async def get_provider(id: int, service: ProviderServiceDep) -> GetProvider:
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
    return {
        "access_token": token,
        "token_type": "JWT",
        "exp_time": expiry_in_seconds,
    }


@router.get("/logout")
async def logout_provider(token_data: Annotated[dict, Depends(get_access_token)]):
    return {"Token UUID": token_data["jti"]}


@router.get("/token/verify")
async def verify_provider_token(
    token: Annotated[str, Depends(oauth2_scheme)], service: ProviderServiceDep
) -> dict:

    decoded_token = token_decoder(token)

    if decoded_token is None:
        raise HTTPException(
            detail="Invalid Token, Please Provide valid Token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    provider_data = await service.get_provider(decoded_token["user"]["id"])

    return {
        "message": "User Authenticated Successfully..!!",
        "Provider_Details": provider_data.model_dump(exclude={"ProviderPassword"}),
    }
