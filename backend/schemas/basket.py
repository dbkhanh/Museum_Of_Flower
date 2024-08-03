from pydantic import BaseModel

class BasketBase(BaseModel):
    total_tickets: int

class BasketCreate(BasketBase):
    pass

class Basket(BasketBase):
    basket_id: int

    class Config:
        from_attributes = True
