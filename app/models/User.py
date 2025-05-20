from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
	__tablename__ = "tb_user"

	user_id = Column(Integer, primary_key = True, index=True)
	user_name = Column(String(255))
	user_email = Column(String(255), unique=True)
	hashed_password = Column(String(255), nullable=False)
	company_name = Column(String(255))
	role = Column(String(10), nullable=False)
	status = Column(Boolean, default=True)
	phone = Column(String(10))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default = 'admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default = 'admin')
	
	# set relationship
	orders = relationship('Order', back_populates='user')