from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    purchase_date = Column(TIMESTAMP, server_default=func.now())
    price = Column(DECIMAL(5, 2), nullable=False)
    basket_id = Column(Integer, ForeignKey("basket.basket_id"), nullable=True)

    basket = relationship("Basket", back_populates="tickets")

class Basket(Base):
    __tablename__ = "basket"

    basket_id = Column(Integer, primary_key=True, index=True)
    total_tickets = Column(Integer, default=0)

    tickets = relationship("Ticket", back_populates="basket")
