from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, DateTime
from sqlalchemy import Enum as SqlaEnum
from backend.database import Base
from datetime import datetime
from enum import Enum
from datetime import datetime

class TicketType(Enum):
    GENERAL_ADMISSION = "General Admission"
    GUIDED_TOUR = "Guided Tour"
    ANNUAL_PASS = "Annual Pass"

class TicketSubtype(Enum):
    ADULT = "Adult"
    CHILDREN = "Children"
    SENIOR = "Senior"
    INDIVIDUAL = "Individual"
    FAMILY = "Family"
    
class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    type = Column(SqlaEnum(TicketType), nullable=False)
    subtype = Column(SqlaEnum(TicketSubtype), nullable=False)
    purchase_date = Column(DateTime, default=datetime, nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    basket_id = Column(Integer, ForeignKey("baskets.basket_id"), nullable=True)
