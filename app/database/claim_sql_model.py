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
    ClaimUniqueId: str
    ClaimTin: str
    ClaimPlaceOfService: str
    ClaimAuditTime: datetime = Field(sa_type=DateTime(timezone=True))
    ClaimProviderId: UUID = Field(foreign_key="provider.ProviderId")

    Provider: "Provider" = Relationship(
        back_populates="Claims",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    # Format ClaimDate and ClaimCloseEstimation
    # @field_serializer("ClaimDate", "ClaimCloseEstimation", "ClaimAuditTime")
    # def serialize_claim_date(self, dt: datetime) -> str:
    #     return dt.strftime("%d %b %Y, %I:%M %p")


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

    ProviderMail: EmailStr
    ProviderPassword: str
    TIN: str
    Claims: list["Claims"] = Relationship(
        back_populates="Provider",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
