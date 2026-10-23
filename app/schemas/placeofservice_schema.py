from pydantic import BaseModel, Field


class PlaceOfService(BaseModel):
    PlaceOfServiceCd: str = Field(primary_key=True)
    PlacePinCode: str
    PlaceDistrict: str
    PlaceState: str

    model_config = {"from_attributes": True}
