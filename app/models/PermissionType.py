from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class PermissionType(Base):
	__tablename__ = 'tb_permission_type'

	permission_type_id = Column(Integer, primary_key=True, index=True)
	permission_type_name = Column(String(100), nullable = False, unique = True)
	description = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(50), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(50), default='admin')

	# Set relationship
	permissions = relationship("Permission", back_populates='permission_type', cascade='all, delete-orphan')