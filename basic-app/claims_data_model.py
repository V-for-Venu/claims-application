from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_serializer


class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class AddClaimData(BaseModel):
    ClaimName: str
    ClaimAmount: float
    ClaimDate: datetime = Field(
        default=(datetime.now(tz=timezone.utc) - timedelta(days=90))
    )
    ClaimCloseEstimation: datetime = Field(
        default=(datetime.now(tz=timezone.utc) + timedelta(days=10))
    )
    ClaimTPA: str
    ClaimUniqueId: str
    ClaimTin: str
    ClaimPlaceOfService: str
    ClaimAuditTime: datetime = Field(default=(datetime.now(tz=timezone.utc)))


class ClaimResponse(BaseModel):
    ClaimId: int
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: datetime
    ClaimCloseEstimation: datetime
    ClaimUniqueId: str
    ClaimPlaceOfService: str
    ClaimTPA: str
    ClaimTin: str
    ClaimAuditTime: datetime

    @classmethod
    def from_claim_tuple(cls, row: tuple):
        if not row:
            return None
        return cls(
            ClaimId=row[0],
            ClaimName=row[1],
            ClaimAmount=row[2],
            ClaimDate=row[3],
            ClaimStatus=row[4],
            ClaimCloseEstimation=row[5],
            ClaimTPA=row[6],
            ClaimUniqueId=row[7],
            ClaimTin=row[8],
            ClaimPlaceOfService=row[9],
            ClaimAuditTime=row[10],
        )

    # Format ClaimDate and ClaimCloseEstimation
    @field_serializer("ClaimDate", "ClaimCloseEstimation")
    def serialize_claim_date(self, dt: datetime) -> str:
        return dt.strftime("%d %b %Y, %I:%M %p")


class UpdateClaim(BaseModel):
    ClaimStatus: ClaimStatus
    ClaimAuditTime: datetime = Field(default=datetime.now(tz=timezone.utc))
