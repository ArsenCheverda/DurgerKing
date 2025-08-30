from contextlib import asynccontextmanager
from typing import List, Optional

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq

# --- Pydantic Models for API data validation ---

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class PlaceOrder(BaseModel):
    tg_id: int
    first_name: str
    items: List[OrderItem]
    comment: Optional[str] = None
    total_price: float

@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Initializes the database connection on startup."""
    await init_db()
    print('Durger King API is ready!')
    yield

app = FastAPI(title="Durger King API", lifespan=lifespan)

# --- CORS Middleware ---
# Allows the frontend application to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # In production, you should restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.post("/api/order")
async def place_order(order: PlaceOrder):
    """
    Receives an order from the frontend, finds or creates a user,
    and saves the order to the database.
    """
    user = await rq.add_user(order.tg_id, order.first_name)
    await rq.add_order(
        user_id=user.id,
        items=order.items,
        comment=order.comment,
        total_price=order.total_price
    )
    # Here you could also trigger a notification to the restaurant
    print(f"Received new order from user {user.tg_id} for ${order.total_price}")
    return {'status': 'ok', 'message': 'Order placed successfully!'}
