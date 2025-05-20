from pydantic import BaseModel

class CreateProduct(BaseModel):
	product_name : str
	category_id : int 
	description : str | None = None 
	sku_partnumber : str | None = None 
	price : float 
	maximum_discount : float

class UpdateProduct(BaseModel):
	product_id : int
	product_name : str | None = None
	category_id : int | None = None
	description : str | None = None 
	sku_partnumber : str | None = None 
	price : float | None = None
	maximum_discount : float | None = None
	status : bool | None = False