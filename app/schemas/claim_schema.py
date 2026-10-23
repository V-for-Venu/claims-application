from datetime import UTC, datetime, timedelta
from enum import Enum
from uuid import UUID

from database.claim_sql_model import ClaimStatusEnum
from pydantic import BaseModel, Field, field_serializer

from schemas.placeofservice_schema import PlaceOfService as PlaceOfServiceSchema
from schemas.provider_schema import GetProvider


class ClaimStatus(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class AddClaimData(BaseModel):
    ClaimName: str
    ClaimAmount: float
    ClaimDate: datetime = Field(default=(datetime.now(tz=UTC) - timedelta(days=90)))
    ClaimCloseEstimation: datetime = Field(
        default=(datetime.now(tz=UTC) + timedelta(days=10))
    )
    ClaimTPA: str
    ClaimUniqueId: str
    ClaimTin: str
    ClaimPlaceOfService: str
    ClaimAuditTime: datetime = Field(default=(datetime.now(tz=UTC)))


class ClaimResponse(BaseModel):
    ClaimId: UUID
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatusEnum
    ClaimDate: datetime
    ClaimCloseEstimation: datetime
    ClaimUniqueId: str
    ClaimPlaceOfService: str
    ClaimTPA: str
    ClaimTin: str
    ClaimAuditTime: datetime
    ClaimProviderId: UUID
    Provider: GetProvider
    PlaceOfService: PlaceOfServiceSchema

    model_config = {"from_attributes": True}

    # Format ClaimDate, ClaimCloseEstimation and ClaimAuditTime
    @field_serializer("ClaimDate", "ClaimCloseEstimation", "ClaimAuditTime")
    def serialize_claim_date(self, dt: datetime) -> str:
        return dt.strftime("%d %b %Y, %I:%M %p")


class UpdateClaim(BaseModel):
    ClaimStatus: ClaimStatus
    ClaimAuditTime: datetime = Field(default=datetime.now(tz=UTC))
