from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel


class ClaimStatusEnum(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class ProviderTypeEnum(str, Enum):
    Hospital = "Hospital"
    Clinic = "Clinic"
    Pharmacy = "Pharmacy"
    Laboratory = "Laboratory"
    Other = "Other"


class Claims(SQLModel, table=True):
    __tablename__ = "claims"

    ClaimId: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    ClaimName: str
    ClaimAmount: float
    ClaimDate: datetime = Field(sa_type=DateTime(timezone=True))
    ClaimStatus: ClaimStatusEnum = Field(
        sa_type=SQLEnum(
            ClaimStatusEnum, name="claimstatus", native_enum=False, create_type=True
        )
    )
    ClaimCloseEstimation: datetime = Field(sa_type=DateTime(timezone=True))
    ClaimTPA: str
    ClaimTin: str
    ClaimPlaceOfService: str = Field(foreign_key="placeofservice.PlaceOfServiceCd")
    ClaimAuditTime: datetime = Field(sa_type=DateTime(timezone=True))
    ClaimProviderId: UUID = Field(foreign_key="provider.ProviderId")

    Provider: "Provider" = Relationship(
        back_populates="Claims",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    PlaceOfService: "PlaceOfService" = Relationship(
        back_populates="Claims",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Provider(SQLModel, table=True):
    __tablename__ = "provider"

    ProviderId: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    ProviderName: str
    ProviderMail: EmailStr = Field(unique=True, index=True)
    ProviderPassword: str
    ProviderType: ProviderTypeEnum = Field(
        sa_type=SQLEnum(
            ProviderTypeEnum, name="ProviderType", native_enum=False, create_type=True
        )
    )
    TIN: str
    Claims: list["Claims"] = Relationship(
        back_populates="Provider",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class PlaceOfService(SQLModel, table=True):
    PlaceOfServiceCd: str = Field(primary_key=True)
    PlacePinCode: str
    PlaceDistrict: str
    PlaceState: str

    Claims: list["Claims"] = Relationship(
        back_populates="PlaceOfService",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
