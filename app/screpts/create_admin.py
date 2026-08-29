from app.models.user import User
from app.auth.security import password_hash
from app.services.user_service import exist_email,exist_username

from app.database.database import sessionLocal
from app.enums.user_enum import UserEnum



db=sessionLocal()
try:
    un = input("Enter username: ")
    exist_username(db,un)
    em = input("Enter email: ")
    exist_email(db,em)
    phone_no = input("Enter phone number: ")
    password = input("Enter password: ")
    hashed_pw = password_hash(password)



    admin = User(
        username=un,
        email=em,
        hashed_password = hashed_pw,
        role = UserEnum.Admin,
        phone_number=phone_no
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("created admin successfully")
except Exception as e:
    db.rollback()
    print(e)
finally:
    db.close()