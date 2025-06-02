from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Type(Base):
	__tablename__ = 'tb_type'

	type_id = Column(Integer, primary_key = True, index = True)
	type_name = Column(String(255), nullable = False, unique=True)
	description = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)
	created_by = Column(String(255), default='admin')
	updated_at = Column(DateTime)
	updated_by = Column(String(255))

	# set relationship
	category = relationship('Category', back_populates='tb_type', cascade="all, delete-orphan")