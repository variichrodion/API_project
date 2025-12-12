from sqlmodel import *
from datetime import datetime
from typing import Optional, List

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/restaurant_db"
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None)

    addresses: List["Address"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")


class Address(SQLModel, table=True):
    __tablename__ = "addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None)

    user: Optional[User] = Relationship(back_populates="addresses")
    orders: List["Order"] = Relationship(back_populates="address")


class Menu(SQLModel, table=True):
    __tablename__ = "menus"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None)

    restaurants: List["Restaurant"] = Relationship(back_populates="menu")
    dishes: List["Dish"] = Relationship(back_populates="menu")


class Restaurant(SQLModel, table=True):
    __tablename__ = "restaurants"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None
    menu_id: Optional[int] = Field(default=None, foreign_key="menus.id")
    created_at: Optional[datetime] = Field(default=None)

    menu: Optional[Menu] = Relationship(back_populates="restaurants")
    orders: List["Order"] = Relationship(back_populates="restaurant")


class Dish(SQLModel, table=True):
    __tablename__ = "dishes"

    id: Optional[int] = Field(default=None, primary_key=True)
    menu_id: int = Field(foreign_key="menus.id")
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = Field(default=None)

    menu: Optional[Menu] = Relationship(back_populates="dishes")
    order_items: List["OrderItem"] = Relationship(back_populates="dish")


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    restaurant_id: int = Field(foreign_key="restaurants.id")
    address_id: int = Field(foreign_key="addresses.id")
    status: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    user: Optional[User] = Relationship(back_populates="orders")
    restaurant: Optional[Restaurant] = Relationship(back_populates="orders")
    address: Optional[Address] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    dish_id: int = Field(foreign_key="dishes.id")
    quantity: int
    price_at_order: float

    order: Optional[Order] = Relationship(back_populates="items")
    dish: Optional[Dish] = Relationship(back_populates="order_items")

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    amount: float
    method: Optional[str] = None
    status: Optional[str] = None
    paid_at: Optional[datetime] = None

    order: Optional[Order] = Relationship(back_populates="payments")