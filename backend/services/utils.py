from models.Models import UserModel, LeadsModel
from db.base import Base, engine
def create_database():
    Base.metadata.create_all(bind=engine)

create_database()