from pydantic import BaseModel, Field
from typing import Optional


class FeedbackCreate(BaseModel):
    reason: str
    place_id: Optional[int] = Field(None)
    lat: Optional[float] = Field(None)
    lon: Optional[float] = Field(None)