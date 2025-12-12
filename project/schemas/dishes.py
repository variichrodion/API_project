from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DishBase(BaseModel):
    menu_id: int
    name: str
    price: float
    description: Optional[str] = None


class DishCreate(DishBase):
    pass


class DishRead(DishBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True