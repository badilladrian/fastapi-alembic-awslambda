from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.api import deps


from app.cruds.notes import crud_note
from app.schemas import notes as schemas

router = APIRouter()

# Get list of Notes
@router.get("/", response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db_local)) -> Any:
    """
    Get list of Notes.
    """
    notes = crud_note.get_multi(db, skip=skip, limit=limit)
    return notes


# Get Note
@router.get("/{id}", response_model=schemas.Note)
def read_note(*, db: Session = Depends(deps.get_db_local), id: int,) -> Any:
    """
    Get item by ID.
    """
    note = crud_note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Item not found")
    return note


# Create Note
@router.post("/", response_model=schemas.Note)
def create_note(*, db: Session = Depends(deps.get_db_local), note_in: schemas.NoteCreate,) -> Any:
    """
    Create new item.
    """
    note = crud_note.create(db=db, obj_in=note_in)
    return note


# Update Note
@router.put("/{id}", response_model=schemas.Note)
def update_item(*, db: Session = Depends(deps.get_db_local), id: int, note_in: schemas.NoteUpdate,) -> Any:
    """
    Update an item.
    """
    note = crud_note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Item not found")
    note = crud_note.update(db=db, db_obj=note, obj_in=note_in)
    return note


# Get Note
@router.delete("/{id}", response_model=schemas.Note)
def delete_note(*, db: Session = Depends(deps.get_db_local), id: int,) -> Any:
    """
    Delete an item.
    """
    note = crud_note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Item not found")
    note = crud_note.remove(db=db, id=id)
    return note
