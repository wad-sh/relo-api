from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user,requires_admin
from app.schemas.histroy_schemas import HistoryResponse
from app.database.database import get_db
from app.services.history_service import get_by_order
from app.models.user import User
from typing import List

history_router=APIRouter(
    prefix="/history-orders",
    tags=["History"]
)

@history_router.get("/{order_id}",response_model=List[HistoryResponse])
def get (order_id:int,db:Session =Depends(get_db),admin= Depends(requires_admin)):
    return get_by_order(db,order_id)