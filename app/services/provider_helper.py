from bcrypt import checkpw, gensalt, hashpw
from core.exceptions import EntityNotFoundError, InvalidCredentials, InvalidRequestError
from database.claim_sql_model import Provider
from schemas.provider_schema import GetProvider, RegisterProvider
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import token_generator

DUMMY_HASH = "$2b$12$bTI0HmfW.gOy.5c2yJWxbOi2HF.LdLYmxPfWHfGjbGIG0Srp1WIn6"


class ProviderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_provider(self, id) -> GetProvider:
        provider_data = await self.session.get(Provider, id)
        if not provider_data:
            raise EntityNotFoundError
        return provider_data

    async def create_provider(self, provider_data: RegisterProvider) -> Provider:
        hashed_password = hashpw(
            provider_data.ProviderPassword.encode(), gensalt(rounds=12)
        ).decode()
        new_provider = Provider(
            **provider_data.model_dump(exclude=["ProviderPassword", "ProviderType"]),
            ProviderPassword=hashed_password,
            ProviderType=provider_data.ProviderType.value,
        )

        if not new_provider:
            raise InvalidRequestError

        self.session.add(new_provider)
        await self.session.commit()
        await self.session.refresh(new_provider)

        return new_provider

    async def authenticate_provider(self, email: str, password: str) -> str:
        result = await self.session.execute(
            select(Provider).where(Provider.ProviderMail == email)
        )
        provider_data = result.scalar()
        stored_password = (
            provider_data.ProviderPassword if provider_data else DUMMY_HASH
        )
        if not provider_data or not await self.authenticator(stored_password, password):
            raise InvalidCredentials

        token = token_generator(
            provider_data={
                "user": {
                    "name": provider_data.ProviderName,
                    "id": str(provider_data.ProviderId),
                }
            }
        )

        return token

    async def update_provider(self, payload: RegisterProvider, id: int):
        provider_data = await self.get_provider(id)
        if provider_data:
            print("Update")
            await self.session.commit()
            await self.session.refresh(provider_data)
            return True
        else:
            return None

    async def delete_provider(self, id: int):
        provider_data = await self.get_provider(id)
        if provider_data:
            await self.session.delete(provider_data)
            await self.session.commit()
            return True
        else:
            return None

    async def authenticator(self, stored_password, password):
        return checkpw(password.encode(), stored_password.encode())
