from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.models.ticket import TicketType, TicketSubtype


class TicketBase(BaseModel):
    type: TicketType
    subtype: TicketSubtype
    price: float
    basket_id: Optional[int] = None

class TicketCreate(BaseModel):
    type: TicketType
    subtype: TicketSubtype
    purchase_date: Optional[datetime] = None
    price: float
    basket_id: Optional[int] = None
    
    class Config:
        orm_mode = True

class Ticket(TicketBase):
    ticket_id: int
    purchase_date: datetime

    class Config:
        from_attributes = True


