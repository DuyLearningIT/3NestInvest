from pydantic import BaseModel

class UserCreate(BaseModel):
	user_name : str
	user_email: str
	company_name : str
	password : str
	role_id : int

class UserLogin(BaseModel):
	user_email: str
	password: str

class UserUpdate(BaseModel):
	user_id : int 
	user_name: str | None = None
	company_name: str | None = None
	status: bool | None = False
	phone : str | None = None

class UserChangePassword(BaseModel):
	user_id : int
	old_password : str
	new_password : str
