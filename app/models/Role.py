from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Role(Base):
	__tablename__= 'tb_role'

	role_id = Column(Integer, primary_key = True, index = True)
	role_name = Column(String(100), unique = True, nullable = True)
	description = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default='admin')

	# Set relationship
	role_permission = relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')
	users = relationship('User', back_populates= 'role', cascade ='all, delete-orphan')
	products = relationship('Product', back_populates='role')