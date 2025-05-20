from pydantic import BaseModel

class CRUDType(BaseModel):
	type_name : str
	description: str

class UpdateType(BaseModel):
	type_id : int
	type_name: str | None = None
	description : str | None = None
