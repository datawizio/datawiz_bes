from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Client(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    photo: str
    lang: str
    is_staff: bool
    clients: List[Client]

    class Config:
        fields = {"user_id": "id"}
