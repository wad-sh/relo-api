from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user,requires_admin
from app.schemas.trip_schemas import TripCreate,TripResponse,TripStatus,TripUpdateroute,TripUpdateStatus
from app.database.database import get_db
from app.services.trip_service import create_trip,update_route_trip,update_status_admin_trip,update_status_trip,delete_trip
from app.models.user import User

trip_router = APIRouter(
    prefix="/trips",
    tags=["Trip"]
)

@trip_router.post("",response_model=TripResponse)
def create (data: TripCreate,db:Session =Depends(get_db),user: User = Depends(get_current_user) ):
    return create_trip(db,user,data)


@trip_router.put("/{trip_id}/route",response_model=TripResponse)
def update_route (trip_id: int,data: TripUpdateroute,db:Session =Depends(get_db),user: User = Depends(get_current_user)):
    return update_route_trip(db,user,trip_id,data)


@trip_router.put("/{trip_id}/status",response_model=TripResponse)
def update_status (trip_id: int,db:Session =Depends(get_db),user: User = Depends(get_current_user)):
    return update_status_trip(db,user,trip_id)

@trip_router.put("/{trip_id}/status/admin",response_model=TripResponse)
def update_status_admin (data:TripUpdateStatus,trip_id: int,db:Session =Depends(get_db),admin: User = Depends(requires_admin)):
    return update_status_admin_trip(db,trip_id,data)

@trip_router.delete("/{trip_id}",response_model=dict)
def delete (trip_id: int,user: User = Depends(get_current_user),db:Session =Depends(get_db)):
    return delete_trip(db,user,trip_id)