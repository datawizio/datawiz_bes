from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..utils.generics import ListGenericModel


class RoleType(BaseModel):
    id: int
    name: str


class Role(BaseModel):
    id: int
    name: str
    permissions: ListGenericModel[str]
    role_type: RoleType

    model_config = ConfigDict(validate_assignment=True)


class ClientDefaults(BaseModel):
    date_to: datetime
    date_from: datetime
    role: Role

    model_config = ConfigDict(validate_assignment=True)


class Client(BaseModel):
    id: int
    name: str
    defaults: Optional[ClientDefaults]

    model_config = ConfigDict(validate_assignment=True)


class User(BaseModel):
    id: int = Field(alias="user_id")
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    photo: Optional[str]
    lang: str
    is_staff: bool = False
    clients: ListGenericModel[Client] = Field(default_factory=ListGenericModel[Client])

    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
    )
