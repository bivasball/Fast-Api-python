from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database,oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    

     #return {"username": user_credentials.username}
    access_token = oauth2.create_access_token(data={"user_id": "30"})

    return {"access_token": access_token, "token_type": "bearer"}
