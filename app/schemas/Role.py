from pydantic import BaseModel
from typing import List

class RoleCreate(BaseModel):
	role_name : str
	role_description: str | None = None
	permissions: List[int] = []

class RoleUpdate(BaseModel):
	role_id : int 
	role_name : str | None = None
	role_description : str | None = None 
	permissions: List[int] = []
