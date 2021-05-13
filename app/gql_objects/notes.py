# GraphQL
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

# Models
from app.models.notes import Note


class NoteType(SQLAlchemyObjectType):
    class Meta:
        model = Note


class NoteTypeRelay(SQLAlchemyObjectType):
    class Meta:
        model = Note
        interfaces = (relay.Node,)
