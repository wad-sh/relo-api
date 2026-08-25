from pydantic import BaseModel,ConfigDict
from app.enums.order import OrderStatus
from datetime import datetime

class HistoryResponse (BaseModel) :
    id : int
    order_id : int
    old_status : OrderStatus
    new_status: OrderStatus
    changed_at: datetime
    changed_by_id:int
    model_config = ConfigDict(from_attributes=True)