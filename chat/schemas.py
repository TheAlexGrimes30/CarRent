from datetime import datetime

from pydantic import BaseModel


class Messages(BaseModel):
    id: int
    user_id: int
    message: str
    written_at: datetime

    class Config:
        orm_mode = True
