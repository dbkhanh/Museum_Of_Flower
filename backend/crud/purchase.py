from sqlalchemy.orm import Session
from backend import models, schemas

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    db_purchase = models.Purchase(
        basket_id=purchase.basket_id,
        total_tickets=purchase.total_tickets,
        total_amount=purchase.total_amount,
        items_json=purchase.items_json
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_purchases_by_basket(db: Session, basket_id: int):
    return db.query(models.Purchase).filter(models.Purchase.basket_id == basket_id).order_by(models.Purchase.created_at.desc()).all()
