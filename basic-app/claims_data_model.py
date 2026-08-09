from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel, Field


class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Initiated = "Initiated"


class AddClaimData(BaseModel):
    ClaimName: str
    ClaimAmount: float
    ClaimDate: datetime = Field(default=(datetime.now(tz=timezone.utc)-timedelta(days=90)))


class ClaimResponse(BaseModel):
    ClaimId: int
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: datetime

    @classmethod
    def from_claim_tuple(cls, row: tuple):
        if not row:
            return None
        return cls(
            ClaimId=row[0],
            ClaimName=row[1],
            ClaimAmount=row[2],
            ClaimStatus=row[3],
            ClaimDate=row[4]
        )