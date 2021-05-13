from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.utils import random_string
from app.cruds.notes import crud_note
from app.models.notes import Note
from app.schemas.notes import NoteCreate


# POST
def test_create_note(client: TestClient, db: Session) -> None:

    data = {"title": random_string(100), "description": random_string(255), "tags": random_string(100)}
    response = client.post(f"{settings.API_HOST}/v1/notes/", json=data,)
    content = response.json()

    assert response.status_code == 200
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["tags"] == data["tags"]
    assert "id" in content


# GET (element)
def test_read_note(client: TestClient, db: Session) -> None:

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_in = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_in)

    response = client.get(f"{settings.API_HOST}/v1/notes/{note.id}",)
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == note.id
    assert content["title"] == note.title
    assert content["description"] == note.description
    assert content["tags"] == note.tags


# GET (list)
def test_read_notes(client: TestClient, db: Session) -> None:

    db.query(Note).delete()

    for _ in range(10):
        title = random_string(100)
        description = random_string(255)
        tags = random_string(100)

        note_in = NoteCreate(title=title, description=description, tags=tags)
        crud_note.create(db=db, obj_in=note_in)

    response = client.get(f"{settings.API_HOST}/v1/notes/",)
    content = response.json()

    assert response.status_code == 200
    assert len(content) == 10


# PUT
def test_update_note(client: TestClient, db: Session) -> None:

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_in = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_in)

    data = {"title": random_string(100), "description": random_string(255), "tags": random_string(100)}

    response = client.put(f"{settings.API_HOST}/v1/notes/{note.id}", json=data,)
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == note.id
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["tags"] == data["tags"]


# DELETE
def test_delete_note(client: TestClient, db: Session) -> None:

    title = random_string(100)
    description = random_string(255)
    tags = random_string(100)

    note_in = NoteCreate(title=title, description=description, tags=tags)
    note = crud_note.create(db=db, obj_in=note_in)
    print("note id: ", note.id)

    response = client.delete(f"{settings.API_HOST}/v1/notes/{note.id}",)
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == note.id
    assert content["title"] == note.title
    assert content["description"] == note.description
    assert content["tags"] == note.tags
