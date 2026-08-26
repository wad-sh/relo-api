from app.enums.driver_modes import DrivingMode
from app.enums.route_enum import Governorate
from pydantic import BaseModel,ConfigDict,EmailStr
from app.enums.assignmentapplication import AssignmenApplicationtStatus
from datetime import datetime

class AssignmentResponse (BaseModel) :
    order_id: int
    driver_id :int
    status:AssignmenApplicationtStatus
    created_at: datetime
    responded_at: datetime|None = None

