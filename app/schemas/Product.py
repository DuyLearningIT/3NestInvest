from pydantic import BaseModel

class CreateProduct(BaseModel):
	product_name : str
	product_role: int
	category_id : int 
	product_description : str | None = None 
	sku_partnumber : str | None = None 
	price : float 
	maximum_discount : float
	channel_cost: float | None = 0

class UpdateProduct(BaseModel):
	product_id : int
	product_name : str | None = None
	product_role : int | None = None
	category_id : int | None = None
	product_description : str | None = None 
	sku_partnumber : str | None = None 
	price : float | None = None
	maximum_discount : float | None = None
	channel_cost: float | None = None
	status : bool | None = False