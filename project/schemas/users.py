from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True