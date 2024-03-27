import sys

sys.path.append("..")

from typing import List

from authentication import PermissionChecker
from database import get_db
from database_crud import item_db_crud as db_crud
from fastapi import APIRouter, Depends, HTTPException
from permissions.models_permissions import Items
from schemas import Item, ItemIn, ItemUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1")


@router.post(
    "/items",
    dependencies=[Depends(PermissionChecker([Items.permissions.CREATE]))],
    response_model=Item,
    summary="Create a new item",
    tags=["Items"],
)
def create_item(item: ItemIn, db: Session = Depends(get_db)):
    """Creates a new item.

    Args:
        item (ItemIn): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """

    try:
        item_created = db_crud.create_item(db, item)
        return item_created
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.get(
    "/items",
    dependencies=[Depends(PermissionChecker([Items.permissions.READ]))],
    response_model=List[Item],
    summary="Get all items",
    tags=["Items"],
)
def get_items(db: Session = Depends(get_db)):
    """Returns all items.

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """

    try:
        items = db_crud.get_items(db)
        return items
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.delete(
    "/items/{item_id}",
    dependencies=[Depends(PermissionChecker([Items.permissions.DELETE]))],
    summary="Delete an item",
    tags=["Items"],
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Deletes an item.

    Args:
        item_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        db_crud.delete_item(db, item_id)
        return {"result": f"Item with ID {item_id} has been deleted successfully!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.patch(
    "/items/{item_id}",
    dependencies=[
        Depends(PermissionChecker([Items.permissions.READ, Items.permissions.UPDATE]))
    ],
    response_model=Item,
    summary="Update an item",
    tags=["Items"],
)
def update_operating_spot(
    item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)
):
    """Updates an item.

    Args:
        item_id (int): _description_
        item_update (ItemUpdate): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        item = db_crud.update_item(db, item_id, item_update)
        return item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
