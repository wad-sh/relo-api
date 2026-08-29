from app.models.driver import Driver
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.models.order import Order
from app.models.driver_application import DriverApplication
from app.enums.order import OrderStatus
from app.services.user_service import exist_user
from app.services.driver_service import valid_driver
from app.enums.driver_modes import DrivingMode as Mode
from app.services.history_service import create_history
from app.enums.application import ApplicationStatus
from datetime import datetime,timezone
from app.schemas.application_schemas import Apply
from app.enums.user_enum import UserEnum

def create_application (db:Session,user:User,data:Apply):
    exist_user(db,user.id)
    if user.role != UserEnum.Customer :
        raise HTTPException(
            status_code=409,
            detail="admins and drivers can't apply"
        )
    no_active_applcations(db,user)
    new_application = DriverApplication(
        applicant_id=user.id,
        vehicle_type = data.vehicle_type,
        vehicle_model=data.vehicle_model,
        vehicle_year=data.vehicle_year,
        vehicle_capacity_kg=data.vehicle_capacity_kg,
        preferred_area=data.preferred_area,
        preferred_route_from=data.preferred_route_from,
        preferred_route_to=data.preferred_route_to,
        description=data.description
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


def get_all_applications_admin (db:Session):
    return db.query(DriverApplication).filter(DriverApplication.status==ApplicationStatus.PENDING).all()

def accept_application_admin (db:Session,admin:User,app_id:int):
    try:
        app = valid_accept_reject(db,app_id)
        app.reviewed_by = admin.id
        app.reviewed_at = datetime.now(timezone.utc)
        app.status=ApplicationStatus.ACCEPTED
        user = db.query(User).filter(User.id == app.applicant_id).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Applicant user not found"
            )
        user.role =UserEnum.Driver
        new_driver = Driver(
        id=user.id
)

        db.add(new_driver)
        db.commit()
        db.refresh(app)
        return app
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="server error"
        )

def reject_application_admin (db:Session,admin:User,app_id:int):
    try:
        app = valid_accept_reject(db,app_id)
        app.reviewed_by = admin.id
        app.reviewed_at = datetime.now(timezone.utc)
        app.status=ApplicationStatus.REJECTED
        db.commit()
        db.refresh(app)
        return app
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="server error"
        )

def get_my_applications (db:Session,user:User) :
    return db.query(DriverApplication).filter(DriverApplication.applicant_id == user.id).all()

def no_active_applcations (db:Session,user:User) :
    act_apps=db.query(DriverApplication).filter(DriverApplication.applicant_id==user.id,
                                                DriverApplication.status == ApplicationStatus.PENDING).first()
    if act_apps is not None:
        raise HTTPException(
            status_code=409,
            detail="you already have a pending application wait for the response"
        )

def valid_accept_reject (db:Session,app_id:int) :
    app = db.query(DriverApplication).with_for_update().filter(DriverApplication.id == app_id,DriverApplication.status == ApplicationStatus.PENDING).first()
    if app is None :
        raise HTTPException(
            status_code=409,
            detail="Application has already been reviewed"
        )
    return app