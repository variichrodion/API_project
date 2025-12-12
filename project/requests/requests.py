from sqlmodel import Session, select
from models import (
    User, Address, Menu, Restaurant, Dish,
    Order, OrderItem, Payment
)
from models import engine

# Общая выборка данных

def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

def get_user_with_addresses(user_id: int):
    with Session(engine) as session:
        query = select(User).where(User.id == user_id)
        user = session.exec(query).first()
        return user, user.addresses

def get_addresses_by_user(user_id: int):
    with Session(engine) as session:
        stmt = select(Address).where(Address.user_id == user_id)
        return session.exec(stmt).all()

def get_menu_with_dishes(menu_id: int):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        return menu, menu.dishes

def get_all_restaurants():
    with Session(engine) as session:
        return session.exec(select(Restaurant)).all()

def get_restaurant_full_menu(restaurant_id: int):
    with Session(engine) as session:
        rest = session.get(Restaurant, restaurant_id)
        dishes = rest.menu.dishes if rest.menu else []
        return rest, dishes

def get_all_orders():
    with Session(engine) as session:
        return session.exec(select(Order)).all()

def get_order_full(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        return {
            "order": order,
            "items": order.items,
            "payment": order.payments
        }

def get_orders_by_user(user_id: int):
    with Session(engine) as session:
        stmt = select(Order).where(Order.user_id == user_id)
        return session.exec(stmt).all()