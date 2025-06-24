from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class ChangeManagement(Base):
	__tablename__ ='tb_change'

	change_id = Column(Integer, primary_key = True, index=True)
	change_description  = Column(String(255), nullable= False)
	date = Column(DateTime, default = datetime.utcnow)
	requested_by = Column(String(255), nullable = False)
