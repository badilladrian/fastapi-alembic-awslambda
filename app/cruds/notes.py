from sqlalchemy.orm import Session

from app.cruds.base import CRUDBase

from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    pass


crud_note = CRUDNote(Note)
