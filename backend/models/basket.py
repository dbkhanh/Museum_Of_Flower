from sqlalchemy import Column, Integer
from backend.database import Base

class Basket(Base):
    __tablename__ = "baskets"

    basket_id = Column(Integer, primary_key=True, index=True)
    total_tickets = Column(Integer, default=0)
