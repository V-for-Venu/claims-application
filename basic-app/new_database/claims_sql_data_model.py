from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date, timedelta


class ClaimStatus(Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"


class Claims(SQLModel, table=True):
    __tablename__ = "claims"
    
    ClaimId: int = Field(primary_key=True, autoincrement=True)
    ClaimName: str
    ClaimAmount: float
    ClaimStatus: ClaimStatus
    ClaimDate: date