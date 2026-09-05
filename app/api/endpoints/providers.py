from fastapi import APIRouter, HTTPException, status
from schemas.provider_schema import RegisterProvider
from services.dependencies import ProviderServiceDep

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
