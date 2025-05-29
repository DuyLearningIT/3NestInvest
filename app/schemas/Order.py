from pydantic import BaseModel
from typing import List 

class OrderDetailCreate(BaseModel):
	product_id: int
	quantity: int 
	price_for_customer: float
	service_contract_duration : int

class OrderCreate(BaseModel):
	order_title : str
	customer_name: str
	adress: str
	billing_address : str
	details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
	order_id : int
	order_title: str | None = None
	order_status: str | None = None
	customer_name: str | None = None
	address: str | None = None
	billing_address: str | None = None