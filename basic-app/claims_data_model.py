from pydantic import BaseModel
from enum import Enum


class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"


class AddClaimData(BaseModel):
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: str