from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, utils, oauth2
from ..database import get_db
from sqlalchemy import text

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    # Use raw SQL query to fetch the user by ID
    query = text(
        "SELECT id, email, created_at FROM fast_api.usersEmailPass WHERE id = :id"
    )
    result = db.execute(query, {"id": id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    # Return user details as a dictionary
    return {"id": result.id, "email": result.email, "created_at": result.created_at}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

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


# ---------------Delete user by id ----#
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Check if user exists
    query = text("SELECT id FROM fast_api.usersEmailPass WHERE id = :id")
    result = db.execute(query, {"id": id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    # Delete user
    delete_query = text("DELETE FROM fast_api.usersEmailPass WHERE id = :id")
    db.execute(delete_query, {"id": id})
    db.commit()  # Ensure changes are saved

    # return statment not required as it is returning 204


@router.put("/", status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    email: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Check if user exists
    query = text("SELECT id FROM fast_api.usersEmailPass WHERE id = :id")
    result = db.execute(query, {"id": id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    # Check if the new email is already taken
    email_check_query = text(
        "SELECT id FROM fast_api.usersEmailPass WHERE email = :email"
    )
    email_exists = db.execute(email_check_query, {"email": email}).fetchone()

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' is already in use.",
        )

    # Update user email
    update_query = text(
        "UPDATE fast_api.usersEmailPass SET email = :email WHERE id = :id"
    )
    db.execute(update_query, {"id": id, "email": email})
    db.commit()  # Save changes

    return {"message": f"The email {email} has been updated for the id {id}"}


# ---------------------PATCH -------for partial update -------------#
@router.patch("/", status_code=status.HTTP_200_OK)
def patch_user(
    id: int,
    email: str = None,  # Optional field for partial updates
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Check if user exists
    query = text("SELECT id, email FROM fast_api.usersEmailPass WHERE id = :id")
    result = db.execute(query, {"id": id}).fetchone()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    # Check if the new email is already taken
    if email:
        email_check_query = text(
            "SELECT id FROM fast_api.usersEmailPass WHERE email = :email"
        )
        email_exists = db.execute(email_check_query, {"email": email}).fetchone()

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{email}' is already in use.",
            )

        # Update only the provided fields
        update_query = text(
            "UPDATE fast_api.usersEmailPass SET email = :email WHERE id = :id"
        )
        db.execute(update_query, {"id": id, "email": email})
        db.commit()  # Save changes

    return {"message": f"The email {email} has been updated for the id {id}"}
