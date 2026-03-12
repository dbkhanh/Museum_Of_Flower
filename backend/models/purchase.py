from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, DECIMAL
from backend.database import Base
from datetime import datetime

class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = Column(Integer, primary_key=True, index=True)
    basket_id = Column(Integer, ForeignKey("baskets.basket_id"), nullable=False, index=True)
    total_tickets = Column(Integer, default=0)
    total_amount = Column(DECIMAL(10, 2), default=0)
    items_json = Column(Text, nullable=True)  # JSON string of items
    created_at = Column(DateTime, default=datetime.now)
