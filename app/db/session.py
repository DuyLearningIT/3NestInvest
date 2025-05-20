from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/3nestinvest'

engine = create_engine(
	DATABASE_URL, 
	echo = True, 
	future = True
)

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind= engine)