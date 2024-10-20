from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_name = "coins_data.db"
engine = create_engine(f"sqlite:///{db_name}", echo=False)
session = sessionmaker(bind=engine)
