from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: EmailStr


class UserResponse(UserBase):
    id: int
    is_active: str
    is_admin: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
