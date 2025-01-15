from pydantic import BaseModel, EmailStr
import datetime


class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: str
    note: str


class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    owner_id: int
    date_created: datetime.datetime
    date_updated: datetime.datetime

    class Config:
        orm_mode = True