from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TicketBase(BaseModel):
    category: str
    basket_id: Optional[int] = None

class TicketCreate(TicketBase):
    price: float

class Ticket(TicketBase):
    ticket_id: int
    purchase_date: datetime

    class Config:
        orm_mode = True

class BasketBase(BaseModel):
    total_tickets: int

class BasketCreate(BasketBase):
    pass

class Basket(BasketBase):
    basket_id: int
    tickets: List[Ticket] = []

    class Config:
        orm_mode = True
