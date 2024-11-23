from datetime import datetime
from pydantic import BaseModel, Field


class BlockUserModel(BaseModel):
    blocked_by_user_id: str
    blocked_user_id: str
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
