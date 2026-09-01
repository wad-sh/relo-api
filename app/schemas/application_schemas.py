from app.enums.application import ApplicationStatus,VehicleType
from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime
from app.enums.route_enum import Governorate

class ApplicationResponse (BaseModel):
    id: int
    applicant_id:int
    created_at:datetime
    status:ApplicationStatus
    reviewed_by :int| None = None
    reviewed_at:datetime| None = None
    model_config = ConfigDict(from_attributes=True)


class Apply (BaseModel) :
    vehicle_type:VehicleType
    vehicle_model:str
    vehicle_year:int =Field(
        ge=1930,
        le=datetime.now().year
    )
    vehicle_capacity_kg:int
    preferred_area:Governorate
    preferred_route_from:Governorate|None=None
    preferred_route_to:Governorate|None=None
    description:str|None=None