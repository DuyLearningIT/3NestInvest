from pydantic import BaseModel

class CreateCategory(BaseModel):
	category_name : str
	category_description : str | None = None
	type_id : int

class UpdateCategory(BaseModel):
	category_id : int
	category_name : str | None = None
	category_description : str | None = None
	type_id : int | None = None