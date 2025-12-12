from sqlmodel import Session, select
from models import (
    User, Address, Menu, Restaurant, Dish,
    Order, OrderItem, Payment
)
from models import engine

# Пользовательские сценарии

def user_get_all_menus():
    with Session(engine) as session:
        return session.exec(select(Menu)).all()

def user_get_menu_dishes(menu_id: int):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        return menu.dishes if menu else []

def user_get_or_create_cart(user_id: int, restaurant_id: int, address_id: int):
    with Session(engine) as session:
        # Ищем существующую корзину
        cart = session.exec(
            select(Order).where(
                Order.user_id == user_id,
                Order.restaurant_id == restaurant_id,
                Order.status == "cart"
            )
        ).first()

        if cart:
            return cart

        # Создаём новую корзину
        cart = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            address_id=address_id,
            status="cart"
        )
        session.add(cart)
        session.commit()
        session.refresh(cart)
        return cart

def user_add_item_to_cart(order_id: int, dish_id: int, qty: int):
    with Session(engine) as session:
        dish = session.get(Dish, dish_id)
        if not dish:
            return None

        item = OrderItem(
            order_id=order_id,
            dish_id=dish_id,
            quantity=qty,
            price_at_order=dish.price
        )

        session.add(item)
        session.commit()
        session.refresh(item)
        return item

def user_remove_item_from_cart(order_item_id: int):
    with Session(engine) as session:
        item = session.get(OrderItem, order_item_id)
        if not item:
            return False

        session.delete(item)
        session.commit()
        return True

def user_view_cart(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)

        total = sum(i.quantity * i.price_at_order for i in order.items)

        return {
            "items": order.items,
            "total": total
        }

def user_checkout(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            return None

        order.status = "created"
        order.updated_at = datetime.now()

        session.add(order)
        session.commit()
        session.refresh(order)
        return order

def user_pay_order(order_id: int, method="card"):
    with Session(engine) as session:
        order = session.get(Order, order_id)

        total = sum(i.quantity * i.price_at_order for i in order.items)

        payment = Payment(
            order_id=order.id,
            amount=total,
            method=method,
            status="paid" if method == "card" else "pending",
            paid_at=datetime.now() if method == "card" else None
        )

        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment

def user_get_order_status(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        return order.status if order else None

def user_order_history(user_id: int):
    with Session(engine) as session:
        stmt = select(Order).where(
            Order.user_id == user_id,
            Order.status != "cart"
        )
        return session.exec(stmt).all()