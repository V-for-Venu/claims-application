from pydantic import BaseModel, Field


class PlaceOfService(BaseModel):
    """Schema for Place of Service"""

    PlaceOfServiceCd: str = Field(primary_key=True)
    PlacePinCode: str
    PlaceDistrict: str
    PlaceState: str

    model_config = {"from_attributes": True}
