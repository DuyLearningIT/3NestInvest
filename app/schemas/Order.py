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
	contact_name: str
	contact_email: str
	contact_phone: str
	address: str
	billing_address : str
	status: str | None = 'draft'
	details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
	order_id : int
	order_title: str | None = None
	status: str | None = None
	customer_name: str | None = None
	address: str | None = None
	billing_address: str | None = None
	contact_name: str | None = None
	contact_email: str | None = None
	contact_phone: str | None = None
	details: List[OrderDetailCreate]