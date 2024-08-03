from sqlalchemy.orm import Session
from backend import models, schemas
from backend.crud.basket import get_basket

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket())
    db.add(db_ticket)
    if ticket.basket_id:
        basket = get_basket(db, ticket.basket_id)
        if basket:
            basket.total_tickets += 1
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
