from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    category: str
    price: float
    basket_id: Optional[int] = None

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    ticket_id: int
    purchase_date: datetime

    class Config:
        from_attributes = True