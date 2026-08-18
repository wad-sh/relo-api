from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.auth.jwt_handler import verify_access_token
from app.enums.user_enum import UserEnum
from fastapi.security import OAuth2PasswordBearer


token_reader = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def get_current_user (db: Session = Depends(get_db),token :str = Depends(token_reader)) :
    payload = verify_access_token(token)
    if payload is None :
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    
    user_id = payload.get("sub")

    if user_id is None :
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
        status_code=401,
        detail="invalid token"
        )

    current_user = db.query(User).filter(User.id == user_id).first()
    
    if current_user is None :
        raise HTTPException(
                status_code=401,
                detail="invalid token"
        )

    return current_user





def requires_admin (current_user: User = Depends(get_current_user)) : 
    if current_user.role != UserEnum.Admin:
        raise HTTPException(
            status_code=403,
            detail="you are not an admin"
        )
    return current_user