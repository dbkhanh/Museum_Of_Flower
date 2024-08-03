from fastapi import FastAPI
from backend.api import basket, ticket
from backend.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(basket.router, prefix="/baskets", tags=["baskets"])
app.include_router(ticket.router, prefix="/tickets", tags=["tickets"])
