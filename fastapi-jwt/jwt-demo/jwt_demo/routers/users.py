from typing import List

from authentication import PermissionChecker, authenticate_user, create_access_token
from database import get_db
from database_crud import user_db_crud as db_crud
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from permissions.models_permissions import Users
from schemas import Token, User, UserSignUp, UserUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1")


@router.post(
    "/users",
    dependencies=[Depends(PermissionChecker([Users.permissions.CREATE]))],
    response_model=User,
    summary="Register a user",
    tags=["Users"],
)
def create_user(user_signup: UserSignUp, db: Session = Depends(get_db)):
    """Register a user.

    Args:
        user_signup (UserSignUp): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        user_created = db_crud.add_user(db, user_signup)
        return user_created
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.get(
    "/users",
    dependencies=[Depends(PermissionChecker([Users.permissions.READ]))],
    response_model=List[User],
    summary="Get all users",
    tags=["Users"],
)
def get_users(db: Session = Depends(get_db)):
    """Returns all users.

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        users = db_crud.get_users(db)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.patch(
    "/users",
    dependencies=[
        Depends(PermissionChecker([Users.permissions.READ, Users.permissions.UPDATE]))
    ],
    response_model=User,
    summary="Update a user",
    tags=["Users"],
)
def update_user(
    user_email: str, user_update: UserUpdate, db: Session = Depends(get_db)
):
    """Updates a user.

    Args:
        user_email (str): _description_
        user_update (UserUpdate): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """

    try:
        user = db_crud.update_user(db, user_email, user_update)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.delete(
    "/users",
    dependencies=[Depends(PermissionChecker([Users.permissions.DELETE]))],
    summary="Delete a user",
    tags=["Users"],
)
def delete_user(user_email: str, db: Session = Depends(get_db)):
    """Delete a user.

    Args:
        user_email (str): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        db_crud.delete_user(db, user_email)
        return {
            "result": f"User with email {user_email} has been deleted successfully!"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.post(
    "/token", response_model=Token, summary="Authorize as a user", tags=["Users"]
)
def authorize(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Logs in a user.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    print(form_data.username)
    print(form_data.password)
    user = authenticate_user(
        db=db, user_email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user email or password.")
    try:
        access_token = create_access_token(data=user.email)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
