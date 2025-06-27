from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class UserRequest(Base):
	__tablename__ = 'tb_user_request'

	request_id = Column(Integer, primary_key=True, index=True)
	user_name = Column(String(255), nullable=False)
	user_email = Column(String(255), nullable=False)
	phone = Column(String(10), nullable=False)
	company_name = Column(String(255), nullable=False)
	status = Column(String(100), default='Pending')

