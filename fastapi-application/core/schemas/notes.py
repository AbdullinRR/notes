from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime


class NoteCreate(BaseModel):
    content: str


class NoteUpdate(BaseModel):
    content: str | None = None

