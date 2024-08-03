from sqlalchemy.orm import Session
from backend import models, schemas

def get_basket(db: Session, basket_id: int):
    return db.query(models.Basket).filter(models.Basket.basket_id == basket_id).first()

def create_basket(db: Session, basket: schemas.BasketCreate):
    db_basket = models.Basket(total_tickets=basket.total_tickets)
    db.add(db_basket)
    db.commit()
    db.refresh(db_basket)
    return db_basket
