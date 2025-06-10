from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
# from app.core import DATABASE_URL

DATABASE_URL = 'mysql+pymysql://admin:NguyenQuangDuy@threenest.c1u22ewui7uw.ap-southeast-2.rds.amazonaws.com:3306/3nestinvest'

engine = create_engine(
	DATABASE_URL, 
	echo = True, 
	future = True
)

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind= engine)