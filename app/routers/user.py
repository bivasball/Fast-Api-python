from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy import text

router = APIRouter(prefix="/users", tags=["Users"])

# /users/
# /users


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


@router.get("/", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # Use raw SQL query to fetch the user by ID
    query = text("SELECT id, email, created_at FROM fast_api.usersEmailPass WHERE id = :id")
    result = db.execute(query, {"id": id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )

    # Return user details as a dictionary
    return {
        "id": result.id,
        "email": result.email,
        "created_at": result.created_at
    }


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    query_check = text("SELECT email FROM fast_api.usersEmailPass WHERE email = :email")
    existing_user = db.execute(query_check, {"email": user.email}).fetchone()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    # Hash the password before storing it
    hashed_password = utils.hash(user.password)

    # Call the stored procedure to insert user data
    query = text("CALL fast_api.insert_user_proc(:email, :password)")
    db.execute(query, {"email": user.email, "password": hashed_password})
    db.commit()

    # Fetch newly created user details
    query_select = text(
        "SELECT id, email, created_at FROM fast_api.usersEmailPass WHERE email = :email LIMIT 1"
    )
    result = db.execute(query_select, {"email": user.email}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )

    return {"id": result.id, "email": result.email, "created_at": result.created_at}
