from app.enums.driver_modes import DrivingMode
from app.enums.route_enum import Governorate
from pydantic import BaseModel,ConfigDict,EmailStr
from app.enums.assignment import AssignmentStatus
from datetime import datetime

class AssignmentResponse (BaseModel) :
    order_id: int
    driver_id :int
    status:AssignmentStatus
    created_at: datetime
    responded_at: datetime|None = None
    model_config = ConfigDict(from_attributes=True)

