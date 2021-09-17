from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validate_arguments, Field

from ..utils.generics import ListGenericModel


class RoleType(BaseModel):
    id: int
    name: str


class Role(BaseModel):
    id: int
    name: str
    permissions: ListGenericModel[str]
    role_type: RoleType


class ClientDefaults(BaseModel):
    date_to: datetime
    date_from: datetime
    role: Role


class Client(BaseModel):
    id: int
    name: str
    defaults: Optional[ClientDefaults]

    @validate_arguments
    def set_defaults(self, defaults: Optional[ClientDefaults]):
        self.defaults = defaults


ListClients = ListGenericModel[Client]


class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    photo: Optional[str]
    lang: str
    is_staff: bool = False
    clients: ListClients = Field(default_factory=ListClients)

    class Config:
        fields = {"id": "user_id"}
