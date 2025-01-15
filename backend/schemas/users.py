from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    id: int
    password: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
