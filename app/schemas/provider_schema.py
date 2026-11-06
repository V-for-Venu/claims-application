from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ProviderTypeEnum(str, Enum):
    """Enum for Provider Types"""

    Hospital = "Hospital"
    Clinic = "Clinic"
    Pharmacy = "Pharmacy"
    Laboratory = "Laboratory"
    Other = "Other"


class RegisterProvider(BaseModel):
    """Schema for Registering a New Provider"""

    ProviderName: str = Field(description="Name of the Provider")
    ProviderMail: EmailStr = Field(
        description="Email of the Provider",
        example=["provider@example.com", "provider.hospital@example.com"],
    )
    ProviderPassword: str = Field(description="Password of the Provider")
    ProviderType: ProviderTypeEnum = Field(description="Type of the Provider")
    TIN: str = Field(description="Tax Identification Number of the Provider")


class GetProvider(BaseModel):
    """Schema for Retrieving Provider Details"""

    ProviderId: UUID = Field(description="Unique Identifier for the Provider")
    ProviderName: str = Field(description="Name of the Provider")
    ProviderMail: EmailStr = Field(description="Email of the Provider")
    ProviderType: ProviderTypeEnum = Field(description="Type of the Provider")
    TIN: str = Field(description="Tax Identification Number of the Provider")

    model_config = {"from_attributes": True}
