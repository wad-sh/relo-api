from jose import jwt,JWTError
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY,ALGORITHM
from datetime import datetime,timedelta,timezone






def create_access_token (data: dict) : 
    to_encode = data.copy()
    exp = datetime.now(timezone.utc ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : exp})
    return jwt.encode(to_encode,SECRET_KEY,ALGORITHM)



def verify_access_token (token: str) : 
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None