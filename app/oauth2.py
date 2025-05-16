from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from sqlalchemy import text

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Expriation time


def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    query = text("SELECT * FROM fast_api.usersEmailPass WHERE id = :id")
    result = db.execute(query, {"id": token.id}).fetchone()

    if not result:
        raise credentials_exception

    return result


def verify_access_token(token: str, credentials_exception):
    try:
        # print("Received Token:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("Decoded Payload:", payload)

        id: str = payload.get("user_id")
        if id is None:
            print("User ID missing in token!")
            raise credentials_exception

        # Convert `id` to string before passing it to TokenData
        token_data = schemas.TokenData(id=str(id))

    except JWTError as e:
        print("JWT Error:", e)
        raise credentials_exception
    except Exception as e:
        print("Unexpected Error:", e)
        raise credentials_exception

    return token_data
