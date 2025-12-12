from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Dish
from database import get_session
from schemas.dishes import DishCreate, DishRead

router = APIRouter(prefix="/dishes", tags=["Dishes"])

@router.post("/", response_model=DishRead)
def create_dish(dish: DishCreate, session: Session = Depends(get_session)):
    new_dish = Dish(**dish.dict())
    session.add(new_dish)
    session.commit()
    session.refresh(new_dish)
    return new_dish

@router.get("/{dish_id}", response_model=DishRead)
def get_dish(dish_id: int, session: Session = Depends(get_session)):
    return session.get(Dish, dish_id)

@router.get("/", response_model=list[DishRead])
def list_dishes(session: Session = Depends(get_session)):
    return session.exec(select(Dish)).all()

@router.put("/dishes/{dish_id}")
def update_dish(dish_id: int, updated: Dish):
    with Session(engine) as session:
        dish = session.get(Dish, dish_id)
        if not dish:
            raise HTTPException(404, "Dish not found")

        dish.name = updated.name
        dish.description = updated.description
        dish.price = updated.price
        dish.menu_id = updated.menu_id

        session.commit()
        session.refresh(dish)
        return dish


@router.delete("/dishes/{dish_id}")
def delete_dish(dish_id: int):
    with Session(engine) as session:
        dish = session.get(Dish, dish_id)
        if not dish:
            raise HTTPException(404, "Dish not found")

        session.delete(dish)
        session.commit()
        return {"message": "Dish deleted"}