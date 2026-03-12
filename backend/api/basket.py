from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud import basket as crud_basket, ticket as crud_ticket, purchase as crud_purchase
from backend.schemas.basket import Basket, BasketCreate
from backend.schemas.ticket import Ticket
from backend.schemas.purchase import Purchase, PurchaseCreate
from backend.database import get_db
import json

router = APIRouter()

@router.get("/", response_model=list[Basket])
def list_baskets(db: Session = Depends(get_db)):
    """List all baskets - useful for debugging."""
    return crud_basket.get_all_baskets(db)

@router.post("/", response_model=Basket)
def create_basket(basket: BasketCreate, db: Session = Depends(get_db)):
    return crud_basket.create_basket(db=db, basket=basket)

@router.get("/{basket_id}", response_model=Basket)
def read_basket(basket_id: int, db: Session = Depends(get_db)):
    db_basket = crud_basket.get_basket(db, basket_id=basket_id)
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    return db_basket

@router.get("/{basket_id}/tickets", response_model=list[Ticket])
def read_basket_tickets(basket_id: int, db: Session = Depends(get_db)):
    db_basket = crud_basket.get_basket(db, basket_id=basket_id)
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    return crud_ticket.get_tickets_by_basket(db, basket_id=basket_id)


@router.get("/{basket_id}/purchases", response_model=list[Purchase])
def list_basket_purchases(basket_id: int, db: Session = Depends(get_db)):
    db_basket = crud_basket.get_basket(db, basket_id=basket_id)
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    return crud_purchase.get_purchases_by_basket(db, basket_id=basket_id)


@router.post("/{basket_id}/checkout", response_model=Purchase)
def checkout_basket(basket_id: int, db: Session = Depends(get_db)):
    """Create purchase from current basket contents, then clear basket."""
    db_basket = crud_basket.get_basket(db, basket_id=basket_id)
    if db_basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    tickets = crud_ticket.get_tickets_by_basket(db, basket_id=basket_id)
    if not tickets:
        raise HTTPException(status_code=400, detail="Basket is empty")
    ticket_groups = {}
    total_amount = 0
    for t in tickets:
        key = f"{t.type} - {t.subtype}"
        if key not in ticket_groups:
            ticket_groups[key] = {"count": 0, "price": float(t.price)}
        ticket_groups[key]["count"] += 1
        total_amount += float(t.price)
    items_json = json.dumps(ticket_groups)
    purchase = crud_purchase.create_purchase(db, PurchaseCreate(
        basket_id=basket_id,
        total_tickets=db_basket.total_tickets,
        total_amount=total_amount,
        items_json=items_json
    ))
    crud_basket.clear_basket(db, basket_id)
    return purchase


@router.delete("/{basket_id}/tickets")
def clear_basket(basket_id: int, db: Session = Depends(get_db)):
    if not crud_basket.clear_basket(db, basket_id):
        raise HTTPException(status_code=404, detail="Basket not found")
    return {"status": "cleared"}
