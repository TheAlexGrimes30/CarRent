from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    driving_licence_date: date
    gibdd_number: str
    driving_licence_number: str
    balance: int
    active: bool = True

    class Config:
        orm_mode = True
