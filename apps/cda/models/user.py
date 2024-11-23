import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserOnRegisterModel(BaseModel):
    email: str = Field(max_length=50)
    parola: str


class UserOnLoginModel(UserOnRegisterModel):
    ...


class UserOnAvatarModel(BaseModel):
    avatar: Optional[str] = None


class UserOnUpdateModel(BaseModel):
    nume: Optional[str] = Field(default=None, max_length=50)
    descriere: Optional[str] = Field(default=None, max_length=3000)


class UserOnDbModel(UserOnRegisterModel, UserOnUpdateModel, UserOnAvatarModel):
    created_at: str
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    anunturi_disponibile: int = 1
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class UsersOnResponseModel(UserOnUpdateModel, UserOnAvatarModel):
    user_id: str
