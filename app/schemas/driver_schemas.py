from app.enums.driver_modes import DrivingMode
from app.enums.route_enum import Governorate
from pydantic import BaseModel,ConfigDict,EmailStr
from app.enums.user_enum import UserEnum


class DriverModeUpdate(BaseModel):
    mode: DrivingMode
    operating_area: Governorate | None = None

class OperatingArea (BaseModel) :
    area : Governorate

class DriverResponse (BaseModel) :
    id : int
    username : str
    email : EmailStr
    phone_number : str
    role : UserEnum
    mode : DrivingMode
    local_operating_area  : Governorate| None
    model_config = ConfigDict(from_attributes=True)