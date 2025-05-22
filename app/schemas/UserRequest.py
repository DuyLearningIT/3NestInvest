from pydantic import BaseModel

class CreateRequest(BaseModel):
	user_name : str
	user_email : str
	company_name : str
	phone : str

class UpdateRequest(BaseModel):
	request_id : int
	user_name : str | None = None
	user_email : str | None = None
	company_name : str | None = None
	phone : str | None = None
	status : str | None = None