from typing import List, Optional

from pydantic import BaseModel

# Shared properties
class NoteBase(BaseModel):
    title: str
    description: str
    tags: Optional[str] = None


# Properties to receive on item creation
class NoteCreate(NoteBase):
    pass


# Properties to receive on item update
class NoteUpdate(NoteBase):
    pass


# Properties to return to client
class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True
