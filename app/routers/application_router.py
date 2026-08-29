from fastapi import APIRouter,Depends
from app.services.application_service import get_all_applications_admin,get_my_applications,accept_application_admin,create_application,reject_application_admin
from app.schemas.application_schemas import ApplicationResponse,Apply
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user,requires_admin
from app.models.user import User
from typing import List

application_router = APIRouter(
    prefix="/applications",
    tags=["Driver Applications"]
)

@application_router.post("",response_model=ApplicationResponse)
def create (data:Apply,db:Session = Depends(get_db),user:User=Depends(get_current_user)):
    return create_application(db,user,data)

@application_router.get("/all/admin",response_model=List[ApplicationResponse])
def get_all (db:Session = Depends(get_db),admin:User=Depends(requires_admin)):
    return get_all_applications_admin(db)


@application_router.get("/me",response_model=List[ApplicationResponse])
def get_all (db:Session = Depends(get_db),user:User=Depends(get_current_user)):
    return get_my_applications(db,user)

@application_router.post("/{app_id}/accept",response_model=ApplicationResponse)
def accept (app_id:int,db:Session=Depends(get_db),admin:User = Depends(requires_admin)):
    return accept_application_admin(db,admin,app_id)

@application_router.post("/{app_id}/reject",response_model=ApplicationResponse)
def reject (app_id:int,db:Session=Depends(get_db),admin:User = Depends(requires_admin)):
    return reject_application_admin(db,admin,app_id)