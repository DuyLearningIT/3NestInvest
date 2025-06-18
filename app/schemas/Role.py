from pydantic import BaseModel
from typing import List

class RoleCreate(BaseModel):
	role_name : str
	description: str | None = None
	permissions: List[int] = []

class RoleUpdate(BaseModel):
	role_id : int 
	role_name : str | None = None
	description : str | None = None 
	permissions: List[int] = []
