from pydantic import BaseModel,EmailStr,Field,ConfigDict
from app.enums.user_enum import UserEnum

class UserRegister (BaseModel) :
    username : str =Field(
        min_length=2,
        max_length=30,
        pattern=r"^[a-z0-9_]+$"
    )

    email : EmailStr

    phone_number: str = Field(
            min_length=10, max_length=13
        )

    password : str = Field(
        min_length=8,
        max_length=72
    )

class UserResponse (BaseModel) :
    id : int
    username : str
    email : EmailStr
    phone_number : str
    role : UserEnum
    model_config = ConfigDict(from_attributes=True)

class UserUpdate (BaseModel) :
    username : str | None =Field(
        default=None,
        min_length=2,
        max_length=30,
        pattern=r"^[a-z0-9_]+$"
    )

    email : EmailStr | None = None

class UserPhoneUpdate (BaseModel) :

    phone_number : str  = Field(
        min_length=10,
        max_length=13
    )

class UserPasswordUpdate (BaseModel) :
    password : str  = Field(
        min_length=8,
        max_length=32,
    )
