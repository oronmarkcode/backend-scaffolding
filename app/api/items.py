from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud import create_item, delete_item, get_item, get_items, update_item
from app.database import get_session
from app.models import Item
from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from dependencies import ingest_queue

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse)
def create_new_item(item: ItemCreate, session: Session = Depends(get_session)):
    ingest_queue.put(item.name)
    db_item = create_item(session, item)
    return ItemResponse.from_orm(db_item)


@router.get("/", response_model=List[ItemResponse])
def read_items(session: Session = Depends(get_session)):
    """Get all items"""
    items = get_items(session)
    return [ItemResponse.from_orm(item) for item in items]


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: str, session: Session = Depends(get_session)):
    """Get a specific item by ID"""
    item = get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.from_orm(item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_existing_item(
    item_id: str, item: ItemUpdate, session: Session = Depends(get_session)
):
    """Update an existing item"""
    db_item = update_item(session, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.from_orm(db_item)


@router.delete("/{item_id}")
def delete_existing_item(item_id: str, session: Session = Depends(get_session)):
    """Delete an item (soft delete)"""
    success = delete_item(session, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
