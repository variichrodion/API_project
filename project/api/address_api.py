from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Address
from database import get_session
from schemas.addresses import AddressCreate, AddressRead

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressRead)
def create_address(address: AddressCreate, session: Session = Depends(get_session)):
    new_address = Address(**address.dict())
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    return new_address

@router.get("/{address_id}", response_model=AddressRead)
def get_address(address_id: int, session: Session = Depends(get_session)):
    return session.get(Address, address_id)

@router.get("/", response_model=list[AddressRead])
def list_addresses(session: Session = Depends(get_session)):
    return session.exec(select(Address)).all()