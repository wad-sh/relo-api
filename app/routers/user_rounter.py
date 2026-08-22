from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user
from app.schemas.user_schemas import UserRegister,UserResponse,UserPhoneUpdate,UserUpdate,UserPasswordUpdate
from app.database.database import get_db
from app.schemas.token_schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import create_user,login_user,delete_user,update_password_user,update_phone_user,update_user
from app.models.user import User


user_router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@user_router.post("/register",response_model=UserResponse)
def register (data:UserRegister ,db: Session = Depends(get_db)) :
    return create_user(db,data)


@user_router.post("/login",response_model=Token)
def login (data:OAuth2PasswordRequestForm,db: Session = Depends(get_db)) :
    return login_user(db,data)

@user_router.delete ("/me" , response_model=dict)
def delete (db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return delete_user(db,user)

@user_router.put("/profile",response_model=UserResponse)
def update_email_username (data: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) :
    return update_user(db,user,data)

@user_router.put("/password",response_model=UserResponse)
def update_password (data: UserPasswordUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) :
    return update_password_user(db,user,data)

@user_router.put("/phone",response_model=UserResponse)
def update_phone_number (data: UserPhoneUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) :
    return update_phone_user(db,user,data)