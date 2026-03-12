from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PurchaseBase(BaseModel):
    basket_id: int
    total_tickets: int
    total_amount: float
    items_json: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    purchase_id: int
    created_at: datetime

    class Config:
        from_attributes = True
