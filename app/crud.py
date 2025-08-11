from typing import List

from sqlmodel import Session, select

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


def create_item(session: Session, item: ItemCreate) -> Item:
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_items(session: Session) -> List[Item]:
    statement = select(Item).where(Item.deleted_at.is_(None))
    return session.exec(statement).all()


def get_item(session: Session, item_id: str) -> Item:
    statement = select(Item).where(Item.id == item_id, Item.deleted_at.is_(None))
    return session.exec(statement).first()


def update_item(session: Session, item_id: str, item: ItemUpdate) -> Item:
    db_item = get_item(session, item_id)
    if db_item:
        item_data = item.dict(exclude_unset=True)
        for field, value in item_data.items():
            setattr(db_item, field, value)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    return db_item


def delete_item(session: Session, item_id: str) -> bool:
    db_item = get_item(session, item_id)
    if db_item:
        db_item.deleted_at = db_item.updated_at
        session.add(db_item)
        session.commit()
        return True
    return False
