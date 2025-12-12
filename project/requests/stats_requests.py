from sqlmodel import Session, select
from models import (
    User, Address, Menu, Restaurant, Dish,
    Order, OrderItem, Payment
)
from models import engine

# Более узконаправленные запросы

def calc_order_total(order_id: int):
    with Session(engine) as session:
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        items = session.exec(stmt).all()
        return sum(i.quantity * i.price_at_order for i in items)

def count_orders_by_user(user_id: int):
    with Session(engine) as session:
        stmt = select(Order).where(Order.user_id == user_id)
        return len(session.exec(stmt).all())

def get_most_ordered_dishes(limit=5):
    with Session(engine) as session:
        stmt = (
            select(Dish.name, OrderItem.quantity)
            .join(Dish, Dish.id == OrderItem.dish_id)
        )
        rows = session.exec(stmt).all()

        stats = {}
        for name, qty in rows:
            stats[name] = stats.get(name, 0) + qty

        return sorted(stats.items(), key=lambda x: x[1], reverse=True)[:limit]