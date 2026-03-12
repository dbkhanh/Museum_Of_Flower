from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud import ticket as crud_ticket
from backend.schemas.ticket import Ticket, TicketCreate
from backend.database import get_db

router = APIRouter()

@router.post("/", response_model=Ticket)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    try:
        return crud_ticket.create_ticket(db=db, ticket=ticket)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud_ticket.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    if not crud_ticket.delete_ticket(db, ticket_id):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "deleted"}

