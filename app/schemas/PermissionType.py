from pydantic import BaseModel


class PermissionTypeCreate(BaseModel):
	permission_type_name : str
	description : str | None = None 


class PermissionTypeUpdate(BaseModel):
	permission_type_id : int
	permission_type_name: str | None = None
	description : str | None = None