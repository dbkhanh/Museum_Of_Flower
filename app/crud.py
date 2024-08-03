from sqlalchemy.orm import Session
from . import models, schemas

def get_basket(db: Session, basket_id: int):
    return db.query(models.Basket).filter(models.Basket.basket_id == basket_id).first()

def create_basket(db: Session, basket: schemas.BasketCreate):
    db_basket = models.Basket(total_tickets=basket.total_tickets)
    db.add(db_basket)
    db.commit()
    db.refresh(db_basket)
    return db_basket

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    if ticket.basket_id:
        basket = get_basket(db, ticket.basket_id)
        if basket:
            basket.total_tickets += 1
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
