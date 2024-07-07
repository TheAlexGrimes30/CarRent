from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
