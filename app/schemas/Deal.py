from pydantic import BaseModel
from typing import List 

class OrderCreate(BaseModel):
	order_title : str | None = None
	deal_id: int
	status : str | None = 'draft'
	total_budget : float 

class DealCreate(BaseModel):
	deal_type : str
	description : str | None = None
	tax_indentification_number : str 
	customer_name : str 
	domain_name: str | None = None 
	contact_name: str | None = None
	contact_email: str | None = None
	contact_phone: str | None = None
	status: str | None = 'draft'
	address : str
	billing_address : str

class DealUpdate(BaseModel):
	deal_id: int
	deal_type : str | None = None
	description : str | None = None
	user_id : int | None = 0
	tax_indentification_number : str | None = None 
	customer_name : str  | None = None
	domain_name: str | None = None 
	contact_name: str | None = None
	contact_email: str | None = None
	contact_phone: str | None = None
	status: str | None = 'draft'
	address : str | None = None
	billing_address : str | None = None

class DealApprove(BaseModel):
	deal_id : int
	status: str | None = 'draft'