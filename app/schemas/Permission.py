from pydantic import BaseModel
from app.models import Permission

class PermissionCreate(BaseModel):
	permission_name : str
	description: str | None = None
	permission_type_id: int
	

class PermissionUpdate(BaseModel):
	permission_id : int
	permission_name : str | None = None
	description : str | None = None
	permission_type_id : int | None = None
