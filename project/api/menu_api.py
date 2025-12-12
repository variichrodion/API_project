from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Menu
from database import get_session
from schemas.menus import MenuCreate, MenuRead

router = APIRouter(prefix="/menus", tags=["Menus"])

@router.post("/", response_model=MenuRead)
def create_menu(menu: MenuCreate, session: Session = Depends(get_session)):
    new_menu = Menu(**menu.dict())
    session.add(new_menu)
    session.commit()
    session.refresh(new_menu)
    return new_menu

@router.get("/{menu_id}", response_model=MenuRead)
def get_menu(menu_id: int, session: Session = Depends(get_session)):
    return session.get(Menu, menu_id)

@router.get("/", response_model=list[MenuRead])
def list_menus(session: Session = Depends(get_session)):
    return session.exec(select(Menu)).all()

@router.put("/menus/{menu_id}")
def update_menu(menu_id: int, updated: Menu):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            raise HTTPException(404, "Menu not found")

        menu.title = updated.title
        menu.description = updated.description

        session.commit()
        session.refresh(menu)
        return menu


@router.delete("/menus/{menu_id}")
def delete_menu(menu_id: int):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            raise HTTPException(404, "Menu not found")

        session.delete(menu)
        session.commit()
        return {"message": "Menu deleted"}