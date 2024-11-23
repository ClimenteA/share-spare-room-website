from datetime import datetime
from pydantic import BaseModel, Field


class MessageAdminModel(BaseModel):
    email: str
    message: str
    added_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
