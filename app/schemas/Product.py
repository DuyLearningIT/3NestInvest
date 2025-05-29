from pydantic import BaseModel

class CreateProduct(BaseModel):
	product_name : str
	product_role: str
	category_id : int 
	description : str | None = None 
	sku_partnumber : str | None = None 
	price : float 
	maximum_discount : float
	channel_cost: float

class UpdateProduct(BaseModel):
	product_id : int
	product_name : str | None = None
	product_role : str | None = None
	category_id : int | None = None
	description : str | None = None 
	sku_partnumber : str | None = None 
	price : float | None = None
	maximum_discount : float | None = None
	channel_cost: float | None = None
	status : bool | None = False