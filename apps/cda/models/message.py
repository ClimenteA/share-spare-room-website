import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MessageOnCreateModel(BaseModel):
    message: str = Field(max_length=300)
    listing_id: str
    to_user_id: str


class MessageOnDbModel(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    poster_user_id: str
    interested_user_id: str
    listing_id: str
    poster_message: Optional[str] = Field(default=None, max_length=300)
    interested_message: Optional[str] = Field(default=None, max_length=300)
    poster_seen_it: bool = False
    interested_seen_it: bool = False
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class MessageOnResponseModel(MessageOnDbModel):
    poster_user_name: str
    interested_user_name: str
    poster_user_avatar: str = None
    interested_user_avatar: str = None
