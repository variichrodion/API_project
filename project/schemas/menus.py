from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MenuCreate(MenuBase):
    pass


class MenuRead(MenuBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True