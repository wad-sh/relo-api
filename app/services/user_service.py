from app.models.user import User
from app.schemas.user_schemas import UserRegister,UserUpdate,UserPasswordUpdate,UserPhoneUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import password_hash,password_verify
from app.auth.jwt_handler import create_access_token
from sqlalchemy import or_
from app.enums.user_enum import UserEnum
from app.models.order import Order
from app.models.trip import Trip
from app.enums.order import OrderStatus
from app.enums.trip import TripStatus
from app.models.driver_application import DriverApplication
from app.enums.assignmentapplication import AssignmenApplicationtStatus
from pydantic import EmailStr



def create_user (db: Session, data : UserRegister) :

    exist_username(db, data.username)
    exist_email(db, data.email)
    
    hashed_pw = password_hash(data.password)
    
    new_user = User(
            username = data.username,
            email = data.email,
            hashed_password = hashed_pw,
            role=UserEnum.Customer
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def login_user (db: Session,data:OAuth2PasswordRequestForm) :
    user = db.query(User).filter(or_(User.email == data.username,User.username== data.username)).first()
    if not user :
        raise HTTPException (
            status_code=401,
            detail="wrong email or password"
        )
    hashed = user.hashed_password
    pw = password_verify (data.password,hashed)
    if not pw :
        raise HTTPException (
                    status_code=401,
                    detail="wrong email/username or password"
                )
    access_token = create_access_token({"sub" : str(user.id)})

    return{
        "access_token" : access_token,
        "token_type" : "bearer"
    }



def delete_user (db: Session,user :User) :
    can_update_or_delete(db, user)

    db.delete(user)
    db.commit()

    return {
    "message": "your account has been deleted"
    }


def update_password_user (db: Session,user :User,data:UserPasswordUpdate) :
    exist_user(db,user.id)
    hashed_pw = password_hash(data.password)
    user.hashed_password = hashed_pw
    db.commit()
    db.refresh(user)
    return user

def update_phone_user (db:Session, user:User, data:UserPhoneUpdate) :
    exist_user(db,user.id)
    user.phone_number = data.phone_number
    db.commit()
    db.refresh(user)
    return user





def update_user (db: Session,user :User,data:UserUpdate) :
    can_update_or_delete(db, user)
    if data.username is None and data.email  is None :
        raise HTTPException (
             status_code= 400,
             detail="no change"
        )

    if data.username is not None and exist_username(db,data.username) == False :
        user.username = data.username

    if data.email is not None and exist_email(db,data.email) == False :
        user.email = data.email

    db.commit()
    db.refresh(user)
    return user
        


def exist_username (db: Session, username: str) :
     ex_un = db.query(User).filter(User.username == username).first()
     if ex_un :
                 raise HTTPException (
                     status_code= 409,
                     detail="username already existed"
                 )
     return False

def exist_email (db: Session, email: EmailStr) :
     ex_em = db.query(User).filter(User.email == email).first()
     if ex_em :
                 raise HTTPException (
                     status_code=409,
                     detail="email already existed"
                 )

     return False

def exist_user(db:Session,user_id:int):
    ex_user = db.query(User).filter(User.id == user_id).first()
        
    if ex_user is None :
            raise HTTPException(
                             status_code= 404,
                             detail="no user has been found"
            )
def can_update_or_delete (db: Session,user: User) :
    exist_user(db,user.id)

    has_accepted_orders = db.query(Order).filter(Order.order_owner_id == user.id, or_(
        Order.status == OrderStatus.ACCEPTED,
        Order.status == OrderStatus.IN_TRANSIT
    )).first()

    if has_accepted_orders is not None :
        raise HTTPException(
            status_code= 409,
            detail="you have orders accepted or in transit"
        )
    
    has_trips = db.query(Trip).filter(Trip.driver_id == user.id, or_( 
        Trip.status == TripStatus.PLANNED , Trip.status == TripStatus.ACTIVE
    )).first()

    if has_trips is not None :
            raise HTTPException(
                status_code= 409,
                detail="you have trips planned or active"
            )

    
    has_orders = db.query(Order).filter(
    Order.driver_id == user.id,
    Order.status.in_([OrderStatus.ACCEPTED, OrderStatus.IN_TRANSIT])).first()

    if has_orders is not None :
            raise HTTPException(
                status_code= 409,
                detail="you have active orders as a driver"
            )

    has_pending_application = db.query(DriverApplication).filter(
        DriverApplication.applicant_id == user.id,
        DriverApplication.status == AssignmenApplicationtStatus.PENDING
    ).first()

    if has_pending_application is not None:
        raise HTTPException(
            status_code=409,
            detail="you have a pending driver application"
        )

    return True