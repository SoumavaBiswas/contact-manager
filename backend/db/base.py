from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from constants.const import DB_URL

engine = create_engine(DB_URL)

LocalSession = sessionmaker(autoflush=False,bind=engine)
Base = declarative_base()

