from bcrypt import gensalt, hashpw
from database.claim_sql_model import Provider
from schemas.provider_schema import (
    RegisterProvider,
)
from sqlalchemy.ext.asyncio import AsyncSession

salt = gensalt(rounds=12)


class ProviderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_provider(self, id) -> Provider:
        return self.session.get(Provider, id)

    async def create_provider(self, provider_data: RegisterProvider) -> Provider:
        hashed_password = hashpw(provider_data.ProviderPassword.encode(), salt).decode()
        new_provider = Provider(
            **provider_data.model_dump(exclude=["ProviderPassword"]),
            ProviderPassword=hashed_password,
        )
        self.session.add(new_provider)
        await self.session.commit()
        await self.session.refresh(new_provider)

        return new_provider

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
