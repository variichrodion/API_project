from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_session
from schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    return user


@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.query(User).all()


@router.put("/users/{user_id}")
def update_user(user_id: int, updated: User):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.name = updated.name
        user.phone = updated.phone
        user.email = updated.email

        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.patch("/users/{user_id}")
def patch_user(user_id: int, updated: dict):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in updated.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

        return {"message": f"User {user_id} deleted successfully"}