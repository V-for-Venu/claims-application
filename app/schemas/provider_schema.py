from pydantic import BaseModel, EmailStr


class RegisterProvider(BaseModel):
    ProviderName: str
    ProviderMail: EmailStr
    ProviderPassword: str
    TIN: str


class GetProvider(BaseModel):
    ProviderId: int
    ProviderName: str
    ProviderMail: EmailStr
    TIN: str
