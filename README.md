# Museum of Flowers

## Overview

A web application for the Museum of Flowers that showcases floral arrangements and allows visitors to purchase tickets online. Users can browse ticket options, add them to a basket, and complete checkout. Purchase history is saved and viewable from the basket.

## Features

- **Home & About** – Museum information and exhibits
- **Tickets** – Three ticket types: General Admission, Guided Tour, and Annual Pass
- **Basket** – Add tickets, remove items, view order summary
- **Checkout** – Confirm purchase and see order confirmation
- **Purchase History** – View previous purchases when clicking the basket icon

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/dbkhanh/Museum_Of_Flower.git
cd Museum_Of_Flower
```

### 2. Set up the environment

**Option A – Poetry (recommended)**

```bash
poetry install
```

**Option B – venv + pip**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure the database

Create a `.env` file in the project root:

```
database_url=sqlite:///./museum.db
```

For PostgreSQL:

```
database_url=postgresql://user:password@localhost:5432/museumofflower
```

### 4. Run the application

```bash
# With Poetry:
poetry run uvicorn backend.main:app --reload

# With venv:
uvicorn backend.main:app --reload
```

The app runs at **http://127.0.0.1:8000**

## API Endpoints

### Baskets
- `GET /baskets/` – List all baskets
- `POST /baskets/` – Create a basket
- `GET /baskets/{basket_id}` – Get basket details
- `GET /baskets/{basket_id}/tickets` – Get tickets in basket
- `GET /baskets/{basket_id}/purchases` – Get purchase history
- `POST /baskets/{basket_id}/checkout` – Complete checkout (creates purchase, clears basket)
- `DELETE /baskets/{basket_id}/tickets` – Clear basket

### Tickets
- `POST /tickets/` – Add a ticket to a basket
- `GET /tickets/{ticket_id}` – Get ticket details
- `DELETE /tickets/{ticket_id}` – Remove a ticket from basket

## Project Structure

```
MuseumOfFlower/
├── backend/
│   ├── api/          # API routes (basket, ticket)
│   ├── core/         # Config, settings
│   ├── crud/         # Database operations
│   ├── models/       # SQLAlchemy models (Basket, Ticket, Purchase)
│   └── schemas/      # Pydantic schemas
├── starter/          # Frontend (HTML, CSS, JS)
│   ├── home.html
│   ├── about.html
│   ├── tickets.html
│   ├── checkout.html
│   ├── basket.js
│   └── app.css
├── .env              # Database URL (create this)
├── pyproject.toml
└── requirements.txt
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite (default) or PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
