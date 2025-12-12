from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Restaurant
from database import get_session
from schemas.restaurants import RestaurantCreate, RestaurantRead

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", response_model=RestaurantRead)
def create_restaurant(restaurant: RestaurantCreate, session: Session = Depends(get_session)):
    new_restaurant = Restaurant(**restaurant.dict())
    session.add(new_restaurant)
    session.commit()
    session.refresh(new_restaurant)
    return new_restaurant

@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    return session.get(Restaurant, restaurant_id)

@router.get("/", response_model=list[RestaurantRead])
def list_restaurants(session: Session = Depends(get_session)):
    return session.exec(select(Restaurant)).all()

@router.put("/restaurants/{rest_id}")
def update_restaurant(rest_id: int, updated: Restaurant):
    with Session(engine) as session:
        rest = session.get(Restaurant, rest_id)
        if not rest:
            raise HTTPException(404, "Restaurant not found")

        rest.name = updated.name
        rest.phone = updated.phone
        rest.menu_id = updated.menu_id

        session.commit()
        session.refresh(rest)
        return rest


@router.delete("/restaurants/{rest_id}")
def delete_restaurant(rest_id: int):
    with Session(engine) as session:
        rest = session.get(Restaurant, rest_id)
        if not rest:
            raise HTTPException(404, "Restaurant not found")

        session.delete(rest)
        session.commit()
        return {"message": "Restaurant deleted"}