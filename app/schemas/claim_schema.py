from datetime import UTC, datetime, timedelta
from enum import Enum
from uuid import UUID

from database.claim_sql_model import ClaimStatusEnum
from pydantic import BaseModel, Field, field_serializer

from schemas.placeofservice_schema import PlaceOfService as PlaceOfServiceSchema
from schemas.provider_schema import GetProvider


class ClaimStatus(str, Enum):
    """Enum for Claim Status"""

    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class AddClaimData(BaseModel):
    """Schema for Adding a New Claim"""

    ClaimName: str = Field(description="Name of the Claim")
    ClaimAmount: float = Field(description="Amount of the Claim")
    ClaimDate: datetime = Field(default=(datetime.now(tz=UTC) - timedelta(days=90)))
    ClaimCloseEstimation: datetime = Field(
        default=(datetime.now(tz=UTC) + timedelta(days=10))
    )
    ClaimTPA: str = Field(description="TPA of the Claim")
    ClaimTin: str = Field(description="TIN of the Claim")
    ClaimPlaceOfService: str = Field(description="Place of Service for the Claim")
    ClaimAuditTime: datetime = Field(default=(datetime.now(tz=UTC)))


class ClaimResponse(BaseModel):
    """Response Schema for Claim Details"""

    ClaimId: UUID = Field(description="Unique Identifier for the Claim")
    ClaimName: str = Field(description="Name of the Claim")
    ClaimAmount: float = Field(description="Amount of the Claim")
    ClaimStatus: ClaimStatusEnum = Field(description="Status of the Claim")
    ClaimDate: datetime = Field(description="Date of the Claim")
    ClaimCloseEstimation: datetime = Field(
        description="Estimated Close Date of the Claim"
    )
    ClaimTPA: str = Field(description="TPA of the Claim")
    ClaimTin: str = Field(description="TIN of the Claim")
    ClaimAuditTime: datetime = Field(description="Audit Time of the Claim")
    Provider: GetProvider = Field(description="Provider associated with the Claim")
    PlaceOfService: PlaceOfServiceSchema | None = Field(
        description="Place of Service for the Claim"
    )

    model_config = {"from_attributes": True}

    # Format ClaimDate, ClaimCloseEstimation and ClaimAuditTime
    @field_serializer("ClaimDate", "ClaimCloseEstimation", "ClaimAuditTime")
    def serialize_claim_date(self, dt: datetime) -> str:
        return dt.strftime("%d %b %Y, %I:%M %p")


class UpdateClaim(BaseModel):
    """Schema for Updating Claim Status"""

    ClaimStatus: ClaimStatus
    ClaimAuditTime: datetime = Field(default=datetime.now(tz=UTC))
