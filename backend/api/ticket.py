from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.crud import ticket as crud_ticket
from backend.schemas.ticket import Ticket, TicketCreate
from backend.database import get_db

router = APIRouter()

@router.post("/tickets/", response_model=Ticket)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return crud_ticket.create_ticket(db=db, ticket=ticket)

