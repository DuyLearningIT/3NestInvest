from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
# from app.core import DATABASE_URL

DATABASE_URL = 'mysql+pymysql://admin:NguyenQuangDuy@dbthreenest.cducasqgky8s.ap-southeast-1.rds.amazonaws.com/dbthreenest'

engine = create_engine(
	DATABASE_URL, 
	echo = False, 
	future = True
)

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind= engine)