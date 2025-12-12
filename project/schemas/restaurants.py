from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    phone: Optional[str] = None
    menu_id: Optional[int] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True