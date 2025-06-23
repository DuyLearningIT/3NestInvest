from pydantic import BaseModel
from typing import List 

class OrderDetailCreate(BaseModel):
	product_id: int
	quantity: int 
	price_for_customer: float
	service_contract_duration : int

class OrderCreate(BaseModel):
	deal_id : int
	order_title : str
	status: str | None = 'draft'
	details: List[OrderDetailCreate]
	order_description: str | None = None

class OrderUpdate(BaseModel):
	order_id : int
	order_title: str | None = None
	status: str | None = None
	details: List[OrderDetailCreate] = []

class OrderApprove(BaseModel):
	order_id : int
	status: str | None = 'draft'
	reason : str | None = None