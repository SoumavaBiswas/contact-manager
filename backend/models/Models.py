from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from passlib import hash
import datetime

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String)
    leads = relationship("LeadsModel", back_populates="owner")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)


class LeadsModel(Base):
    __tablename__ = "leads"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    contact_number = Column(String(10), nullable=False)
    company = Column(String, default="")
    note = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    owner = relationship("UserModel", back_populates="leads")