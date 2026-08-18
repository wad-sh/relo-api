from fastapi import APIRouter,Depends
from sqlalchemy.orm import session
from app.auth.dep import get_current_user
from app.schemas.user_schemas import UserRegister,UserResponse
from app.database.database import get_db
from app.schemas.token_schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import create_user,login_user,delete_user
from app.models.user import User


user_router = APIRouter(
    prefix="/users",
    tags="User"
)

@user_router.post("/register",response_model=UserResponse)
def register (data:UserRegister ,db: session = Depends(get_db)) :
    return create_user(db,data)


@user_router.post("/login",response_model=Token)
def login (data:OAuth2PasswordRequestForm,db: session = Depends(get_db)) :
    return login_user(db,data)

@user_router.delete ("" , response_model=dict)
def delete (db: session = Depends(get_db), user: User = Depends(get_current_user)):
    return delete_user(db,user)