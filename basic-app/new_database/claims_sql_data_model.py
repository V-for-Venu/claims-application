from pydantic import field_serializer
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime


class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class Claims(SQLModel, table=True):
    __tablename__ = "claims"
    
    ClaimId: int = Field(primary_key=True)
    ClaimName: str
    ClaimAmount: float
    ClaimDate: datetime
    ClaimStatus: ClaimStatus
    ClaimCloseEstimation: datetime

    # Format ClaimDate and ClaimCloseEstimation
    @field_serializer("ClaimDate", "ClaimCloseEstimation")
    def serialize_claim_date(self, dt: datetime) -> str:
        return dt.strftime("%d %b %Y, %I:%M %p")