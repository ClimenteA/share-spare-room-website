import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ListingOnCreateModel(BaseModel):
    titlu: str = Field(max_length=75)
    oras: str = Field(max_length=25)
    zona: str = Field(max_length=50)
    descriere: str = Field(max_length=3000)
    pret: int


class ListingOnUpdateModel(ListingOnCreateModel):
    listing_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class ListingOnImageUpdateModel(BaseModel):
    img1: Optional[str] = None
    img2: Optional[str] = None
    img3: Optional[str] = None


class ListingOnDbModel(
    ListingOnUpdateModel,
    ListingOnCreateModel,
    ListingOnImageUpdateModel,
):
    user_id: str
    created_at: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ListingOnResponseModel(ListingOnDbModel):
    user_avatar: Optional[str] = None
    user_nume: Optional[str] = None
    interesati: int = None
