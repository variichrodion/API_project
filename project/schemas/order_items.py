from pydantic import BaseModel


class OrderItemBase(BaseModel):
    order_id: int
    dish_id: int
    quantity: int
    price_at_order: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        from_attributes = True