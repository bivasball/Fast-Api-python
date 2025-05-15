from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # Use raw SQL query to fetch user details
    query = text("SELECT * FROM fast_api.usersemailpass WHERE email = :email LIMIT 1")
    result = db.execute(query, {"email": user_credentials.username}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Extract user details from the query result
    user_id = result.id  # Ensure this matches your database schema
    user_password = result.password

    # Verify user password
    if not utils.verify(user_credentials.password, user_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Create access token
    access_token = oauth2.create_access_token(data={"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}
