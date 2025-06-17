from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ActivityLog(Base):
	__tablename__ = 'tb_activity_log'

	activity_log_id = Column(Integer, index = True, primary_key = True)
	user_id = Column(Integer, ForeignKey('tb_user.user_id'), nullable=False)
	description = Column(String(255))
	created_at = Column(DateTime, default = datetime.utcnow)

	# relationship
	user = relationship('User', back_populates='activity_logs')