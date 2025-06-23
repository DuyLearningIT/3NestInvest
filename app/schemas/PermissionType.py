from pydantic import BaseModel


class PermissionTypeCreate(BaseModel):
	permission_type_name : str
	permission_type_description : str | None = None 


class PermissionTypeUpdate(BaseModel):
	permission_type_id : int
	permission_type_name: str | None = None
	permission_type_description : str | None = None