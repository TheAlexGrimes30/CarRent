from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: Optional[str] = Field(None, max_length=128)
    email: Optional[EmailStr] = Field(None, max_length=64)
    password: Optional[bytes] = Field(None, max_length=128)
    driving_licence_date: Optional[date] = Field(None)
    gibdd_number: Optional[str] = Field(None, max_length=16)
    driving_licence_number: Optional[str] = Field(None, max_length=32)
    balance: Optional[int] = Field(None, gt=0)
    active: bool = True

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        strict = True
        arbitrary_types_allowed = True
