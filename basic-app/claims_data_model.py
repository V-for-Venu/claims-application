from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, timedelta

class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"


class AddClaimData(BaseModel):
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: date = Field(default=(date.today()-timedelta(days=90)))


class ClaimResponse(BaseModel):
    ClaimId: int
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: date

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