from pydantic import BaseModel

class CRUDType(BaseModel):
	type_name : str
	type_description: str

class UpdateType(BaseModel):
	type_id : int
	type_name: str | None = None
	type_description : str | None = None
