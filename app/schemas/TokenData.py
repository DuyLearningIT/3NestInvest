from pydantic import BaseModel

class TokenData(BaseModel):
	user_id : int
	user_name: str
	user_email: str
	role_id: int
	role: str