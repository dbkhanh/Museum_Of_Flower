from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud import basket as crud_basket
from backend.schemas.basket import Basket, BasketCreate
from backend.database import get_db

router = APIRouter()

@router.post("/baskets/", response_model=Basket)
def create_basket(basket: BasketCreate, db: Session = Depends(get_db)):
    return crud_basket.create_basket(db=db, basket=basket)

@router.get("/baskets/{basket_id}", response_model=Basket)
def read_basket(basket_id: int, db: Session = Depends(get_db)):
    db_basket = crud_basket.get_basket(db, basket_id=basket_id)
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    return db_basket
