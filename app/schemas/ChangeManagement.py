from pydantic import BaseModel 

class ChangeCreate(BaseModel):
	change_description: str 
	requested_by: str 

class ChangeUpdate(BaseModel):
	change_id : int
	change_description: str | None = None
	requested_by: str | None = None
