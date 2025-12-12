from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    method: Optional[str] = None
    status: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    paid_at: Optional[datetime]

    class Config:
        from_attributes = True