from pydantic import BaseModel, Field
from typing import List

class FilterPlace(BaseModel):
    categories: List[str] = Field(None),
    types: List[str] = Field(None),
    distance: int = Field(None),
    user_lat: float = Field(),
    user_lon: float = Field()