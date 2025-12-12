from fastapi import FastAPI
from api import user_api, address_api, menu_api, restaurant_api, dish_api, order_api, order_item_api, payment_api
from database import engine
from sqlmodel import SQLModel

app = FastAPI(title="FastFood Restaurant API")

# Создаём таблицы
SQLModel.metadata.create_all(engine)

# Подключаем routers
app.include_router(user_api.router)
app.include_router(address_api.router)
app.include_router(menu_api.router)
app.include_router(restaurant_api.router)
app.include_router(dish_api.router)
app.include_router(order_api.router)
app.include_router(order_item_api.router)
app.include_router(payment_api.router)