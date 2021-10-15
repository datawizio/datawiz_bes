from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..utils.generics import ListGenericModel


class RoleType(BaseModel):
    id: int
    name: str


class Role(BaseModel):
    id: int
    name: str
    permissions: ListGenericModel[str]
    role_type: RoleType

    class Config:
        validate_assignment = True


class ClientDefaults(BaseModel):
    date_to: datetime
    date_from: datetime
    role: Role

    class Config:
        validate_assignment = True


class Client(BaseModel):
    id: int
    name: str
    defaults: Optional[ClientDefaults]

    class Config:
        validate_assignment = True


class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    photo: Optional[str]
    lang: str
    is_staff: bool = False
    clients: ListGenericModel[Client] = Field(default_factory=ListGenericModel[Client])

    class Config:
        validate_assignment = True
        fields = {"id": "user_id"}
