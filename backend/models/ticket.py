from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP
from backend.database import Base
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    purchase_date = Column(TIMESTAMP, default=datetime.utcnow)
    price = Column(DECIMAL(5, 2), nullable=False)
    basket_id = Column(Integer, ForeignKey("baskets.basket_id"), nullable=True)
