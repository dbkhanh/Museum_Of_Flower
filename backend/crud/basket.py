from sqlalchemy.orm import Session
from backend import models, schemas

def get_basket(db: Session, basket_id: int):
    return db.query(models.Basket).filter(models.Basket.basket_id == basket_id).first()

def get_all_baskets(db: Session):
    return db.query(models.Basket).all()

def create_basket(db: Session, basket: schemas.BasketCreate):
    db_basket = models.Basket(total_tickets=basket.total_tickets)
    db.add(db_basket)
    db.commit()
    db.refresh(db_basket)
    return db_basket


def clear_basket(db: Session, basket_id: int) -> bool:
    db_basket = get_basket(db, basket_id)
    if not db_basket:
        return False
    tickets = db.query(models.Ticket).filter(models.Ticket.basket_id == basket_id).all()
    for t in tickets:
        db.delete(t)
    db_basket.total_tickets = 0
    db.commit()
    return True
