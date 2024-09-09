from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from backend.api import basket, ticket
from backend.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(basket.router, prefix="/baskets", tags=["baskets"])
app.include_router(ticket.router, prefix="/tickets", tags=["tickets"])

frontend_directory = os.path.join(os.path.dirname(__file__), '../starter')

app.mount("/static", StaticFiles(directory=frontend_directory), name="static")

@app.get("/", response_class=FileResponse)
async def read_about():
    return os.path.join(frontend_directory, "home.html")
