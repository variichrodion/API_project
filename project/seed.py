from sqlmodel import *
from datetime import *
import random

from models import engine
from models import (
    User,
    Address,
    Menu,
    Restaurant,
    Dish,
    Order,
    OrderItem,
    Payment,
)


def random_phone():
    return "79" + "".join([str(random.randint(0, 9)) for _ in range(9)])

def random_address():
    cities = ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург", "Новосибирск"]
    streets = ["Ленина", "Тверская", "Арбат", "Баумана", "Красная", "Победы"]

    return {
        "city": random.choice(cities),
        "street": random.choice(streets),
        "house": str(random.randint(1, 60)),
        "apartment": str(random.randint(1, 120)),
        "comment": "Комментарий " + str(random.randint(1, 50))
    }


def random_status():
    return random.choice(["created", "delivered", "cancelled"])


def random_payment_method():
    return random.choice(["card", "cash"])


def seed_data():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        print("=== Создание пользователей ===")
        users = []
        for i in range(10):
            u = User(
                name=f"Пользователь {i+1}",
                phone=random_phone(),
                email=f"user{i+1}@example.com",
                created_at=datetime.now()
            )
            users.append(u)
        session.add_all(users)
        session.commit()

        print("=== Создание адресов ===")
        addresses = []
        for user in users:
            for _ in range(random.randint(1, 3)):
                addr_data = random_address()
                addr = Address(
                    user_id=user.id,
                    **addr_data,
                    created_at=datetime.now()
                )
                addresses.append(addr)
        session.add_all(addresses)
        session.commit()

        print("=== Создание меню ===")
        menus = [
            Menu(title="Основное меню", description="Общее меню", created_at=datetime.now()),
            Menu(title="Напитки", description="Прохладительные напитки", created_at=datetime.now()),
            Menu(title="Десерты", description="Сладкое и выпечка", created_at=datetime.now())
        ]
        session.add_all(menus)
        session.commit()

        print("=== Создание ресторанов ===")
        restaurants = [
            Restaurant(name="FastFood №1", phone=random_phone(), menu_id=menus[0].id),
            Restaurant(name="FastFood №2", phone=random_phone(), menu_id=menus[0].id),
            Restaurant(name="FastFood №3", phone=random_phone(), menu_id=menus[0].id),
            Restaurant(name="SweetCake",  phone=random_phone(), menu_id=menus[2].id),
            Restaurant(name="DrinksMix",  phone=random_phone(), menu_id=menus[1].id)
        ]
        session.add_all(restaurants)
        session.commit()

        print("=== Создание блюд ===")
        dishes_data = [
            ("Бургер Классический", 259),
            ("Картофель Фри", 89),
            ("Наггетсы", 149),
            ("Хот-дог Нью-Йоркский", 199),
            ("Кола 0.5", 119),
            ("Спрайт 0.5", 119),
            ("Фанта 0.5", 119),
            ("Чизкейк", 249),
            ("Тирамису", 299),
            ("Кофе Американо", 139),
            ("Кофе Капучино", 169),
            ("Молочный коктейль", 199),
            ("Мисо Суп", 149),
            ("Салат Цезарь", 199),
            ("Пицца Маргарита", 449),
        ]

        dishes = []
        for title, price in dishes_data:
            dish = Dish(
                menu_id=random.choice(menus).id,
                name=title,
                price=price,
                created_at=datetime.now()
            )
            dishes.append(dish)
        session.add_all(dishes)
        session.commit()

        print("=== Создание заказов ===")
        orders = []
        for _ in range(20):
            user = random.choice(users)
            user_addresses = [a for a in addresses if a.user_id == user.id]

            ordr = Order(
                user_id=user.id,
                restaurant_id=random.choice(restaurants).id,
                address_id=random.choice(user_addresses).id,
                status=random_status(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            orders.append(ordr)
        session.add_all(orders)
        session.commit()

        print("=== Создание позиций заказов ===")
        order_items = []
        for order in orders:
            for _ in range(random.randint(1, 4)):
                d = random.choice(dishes)
                item = OrderItem(
                    order_id=order.id,
                    dish_id=d.id,
                    quantity=random.randint(1, 4),
                    price_at_order=d.price
                )
                order_items.append(item)
        session.add_all(order_items)
        session.commit()

        print("=== Создание платежей ===")
        payments = []
        for order in orders:
            items = [i for i in order_items if i.order_id == order.id]
            amount = sum(i.quantity * i.price_at_order for i in items)

            payment = Payment(
                order_id=order.id,
                amount=amount,
                method=random_payment_method(),
                status=random.choice(["paid", "pending"]),
                paid_at=datetime.now() if random.random() < 0.6 else None
            )
            payments.append(payment)

        session.add_all(payments)
        session.commit()

        print("\n=== ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО ДОБАВЛЕНЫ ===")

if __name__ == "__main__":
    seed_data()