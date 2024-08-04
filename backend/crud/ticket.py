from sqlalchemy.orm import Session
from backend import models, schemas
from backend.crud.basket import get_basket

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    basket = None
    if ticket.basket_id:
        basket = get_basket(db, ticket.basket_id)
        if not basket:
            raise ValueError(f"Basket with id {ticket.basket_id} does not exist")

    db_ticket = models.Ticket(
        type=ticket.type,
        subtype=ticket.subtype,
        price=ticket.price,
        basket_id=ticket.basket_id
    )
    db.add(db_ticket)
    
    if basket:
        basket.total_tickets += 1

    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int) -> models.Ticket:
    return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
