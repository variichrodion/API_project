from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None
    comment: Optional[str] = None


class AddressCreate(AddressBase):
    user_id: int


class AddressRead(AddressBase):
    id: int
    user_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True