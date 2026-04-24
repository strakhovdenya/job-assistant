from datetime import datetime

from pydantic import BaseModel, Field


class RawJobCreate(BaseModel):
    raw_text: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1, max_length=100)


class RawJobResponse(BaseModel):
    id: int
    raw_text: str
    source: str
    content_hash: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RawJobListResponse(BaseModel):
    items: list[RawJobResponse]
    total: int
    limit: int
    offset: int