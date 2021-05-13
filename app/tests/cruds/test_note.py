from sqlalchemy.orm import Session

from app.cruds.notes import crud_note
from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteUpdate
from app.tests.utils.utils import random_string

# create
def test_create_note(db: Session) -> None:

    db.query(Note).delete()

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_in = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_in)

    assert note.title == title
    assert note.description == description
    assert note.tags == tags


# get
def test_get_note(db: Session) -> None:

    db.query(Note).delete()

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_in = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_in)

    stored_note = crud_note.get(db=db, id=note.id)
    assert stored_note
    assert note.id == stored_note.id
    assert note.title == stored_note.title
    assert note.description == stored_note.description
    assert note.tags == stored_note.tags


# get_multi
def test_get_notes(db: Session) -> None:

    db.query(Note).delete()

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 0

    for _ in range(10):
        title = random_string(100)
        description = random_string(255)
        tags = random_string(100)

        note_in = NoteCreate(title=title, description=description, tags=tags)
        crud_note.create(db=db, obj_in=note_in)

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 10

    for _ in range(10):
        title = random_string(100)
        description = random_string(255)
        tags = random_string(100)

        note_in = NoteCreate(title=title, description=description, tags=tags)
        crud_note.create(db=db, obj_in=note_in)

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 20


# update
def test_update_note(db: Session) -> None:

    db.query(Note).delete()

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_obj = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_obj)

    assert note.title == title
    assert note.description == description
    assert note.tags == tags

    new_title = random_string(100)
    new_description = random_string(255)
    new_tags = random_string(100)

    note_in = NoteUpdate(title=new_title, description=new_description, tags=new_tags)

    note = crud_note.update(db=db, db_obj=note, obj_in=note_in)

    assert note.title == new_title
    assert note.description == new_description
    assert note.tags == new_tags


# delete
def test_delete_item(db: Session) -> None:
    db.query(Note).delete()

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 0

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_obj = NoteCreate(title=title, description=description, tags=tags)
    note_1 = crud_note.create(db=db, obj_in=note_obj)

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_obj = NoteCreate(title=title, description=description, tags=tags)
    note_2 = crud_note.create(db=db, obj_in=note_obj)

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 2

    id_delete = note_1.id
    crud_note.remove(db=db, id=id_delete)
    note_1 = crud_note.get(db=db, id=id_delete)
    assert note_1 is None

    stored_notes = crud_note.get_multi(db=db)
    assert len(stored_notes) == 1

