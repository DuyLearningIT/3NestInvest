from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
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
	role_id = Column(Integer, ForeignKey('tb_role.role_id', ondelete='CASCADE'), nullable=False)
	status = Column(Boolean, default=True)
	phone = Column(String(10))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default = 'admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default = 'admin')
	
	# set relationship
	deals = relationship('Deal', back_populates='user', cascade="all, delete-orphan" )
	activity_logs = relationship('ActivityLog', back_populates='user', cascade='all, delete-orphan', passive_deletes=True)
	role = relationship('Role', back_populates='users')