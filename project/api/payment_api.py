from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Payment
from database import get_session
from schemas.payments import PaymentCreate, PaymentRead

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, session: Session = Depends(get_session)):
    new_payment = Payment(**payment.dict())
    session.add(new_payment)
    session.commit()
    session.refresh(new_payment)
    return new_payment

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, session: Session = Depends(get_session)):
    return session.get(Payment, payment_id)

@router.get("/", response_model=list[PaymentRead])
def list_payments(session: Session = Depends(get_session)):
    return session.exec(select(Payment)).all()

@router.put("/payments/{payment_id}")
def update_payment(payment_id: int, updated: Payment):
    with Session(engine) as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(404, "Payment not found")

        payment.order_id = updated.order_id
        payment.amount = updated.amount
        payment.method = updated.method
        payment.status = updated.status
        payment.paid_at = updated.paid_at

        session.commit()
        session.refresh(payment)
        return payment


@router.patch("/payments/{payment_id}")
def patch_payment(payment_id: int, updated: dict):
    with Session(engine) as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(404, "Payment not found")

        for key, value in updated.items():
            if hasattr(payment, key) and value is not None:
                setattr(payment, key, value)

        session.commit()
        session.refresh(payment)
        return payment


@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    with Session(engine) as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            raise HTTPException(404, "Payment not found")

        session.delete(payment)
        session.commit()
        return {"message": f"Payment {payment_id} deleted"}