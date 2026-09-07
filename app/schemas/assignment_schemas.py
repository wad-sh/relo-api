
from pydantic import BaseModel,ConfigDict
from app.enums.assignment import AssignmentStatus
from datetime import datetime

class AssignmentResponse (BaseModel) :
    id:int
    order_id: int
    driver_id :int
    status:AssignmentStatus
    created_at: datetime
    responded_at: datetime|None = None
    model_config = ConfigDict(from_attributes=True)

