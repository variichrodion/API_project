from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Order
from database import get_session
from schemas.orders import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderRead)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(**order.dict())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    return session.get(Order, order_id)

@router.get("/", response_model=list[OrderRead])
def list_orders(session: Session = Depends(get_session)):
    return session.exec(select(Order)).all()

@router.patch("/orders/{order_id}")
def update_order(order_id: int, updated: dict):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        for key, value in updated.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)

        session.commit()
        session.refresh(order)
        return order


@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        session.delete(order)
        session.commit()
        return {"message": "Order deleted"}