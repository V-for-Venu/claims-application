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