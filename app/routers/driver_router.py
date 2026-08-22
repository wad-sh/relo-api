from fastapi import APIRouter,Depends
from app.services.driver_service import update_mode_driver,update_area_driver
from app.schemas.driver_schemas import DriverResponse,DriverMode,OperatingArea
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user
from app.models.user import User

driver_router = APIRouter(
    prefix="/drivers",
    tags=["Driver"]
)

@driver_router.put("/mode",response_model=dict)
def update_mode (data:DriverMode ,user:User = Depends(get_current_user),db : Session = Depends(get_db)) :
    return update_mode_driver(db,user,data)

@driver_router.put("/area",response_model=DriverResponse)
def update_area (data:OperatingArea ,user:User = Depends(get_current_user),db : Session = Depends(get_db)) :
    return update_area_driver(db,user,data)