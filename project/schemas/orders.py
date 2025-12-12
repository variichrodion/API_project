from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    restaurant_id: int
    address_id: int
    status: Optional[str] = "new"


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True