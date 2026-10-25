from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ProviderTypeEnum(str, Enum):
    Hospital = "Hospital"
    Clinic = "Clinic"
    Pharmacy = "Pharmacy"
    Laboratory = "Laboratory"
    Other = "Other"


class RegisterProvider(BaseModel):
    ProviderName: str
    ProviderMail: EmailStr
    ProviderPassword: str
    ProviderType: ProviderTypeEnum
    TIN: str


class GetProvider(BaseModel):
    ProviderId: UUID
    ProviderName: str
    ProviderMail: EmailStr
    ProviderType: ProviderTypeEnum
    TIN: str

    model_config = {"from_attributes": True}
