from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import OrderItem
from database import get_session
from schemas.order_items import OrderItemCreate, OrderItemRead

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.post("/", response_model=OrderItemRead)
def create_order_item(item: OrderItemCreate, session: Session = Depends(get_session)):
    new_item = OrderItem(**item.dict())
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@router.get("/{item_id}", response_model=OrderItemRead)
def get_order_item(item_id: int, session: Session = Depends(get_session)):
    return session.get(OrderItem, item_id)

@router.get("/", response_model=list[OrderItemRead])
def list_order_items(session: Session = Depends(get_session)):
    return session.exec(select(OrderItem)).all()

@router.put("/order_items/{item_id}")
def update_order_item(item_id: int, updated: OrderItem):
    with Session(engine) as session:
        item = session.get(OrderItem, item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")

        item.order_id = updated.order_id
        item.dish_id = updated.dish_id
        item.quantity = updated.quantity
        item.price_at_order = updated.price_at_order

        session.commit()
        session.refresh(item)
        return item


@router.patch("/order_items/{item_id}")
def patch_order_item(item_id: int, updated: dict):
    with Session(engine) as session:
        item = session.get(OrderItem, item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")

        for key, value in updated.items():
            if hasattr(item, key) and value is not None:
                setattr(item, key, value)

        session.commit()
        session.refresh(item)
        return item


@router.delete("/order_items/{item_id}")
def delete_order_item(item_id: int):
    with Session(engine) as session:
        item = session.get(OrderItem, item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")

        session.delete(item)
        session.commit()
        return {"message": f"OrderItem {item_id} deleted"}