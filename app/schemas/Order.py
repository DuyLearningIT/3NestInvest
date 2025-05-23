from pydantic import BaseModel
from typing import List 

class OrderDetailCreate(BaseModel):
	product_id: int
	quantity: int 
	discount_percent: float

class OrderCreate(BaseModel):
	order_title : str
	customer_name: str
	details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
	order_id : int
	order_tile: str | None = None
	order_status: str | None = None
	customer_name: str | None = None