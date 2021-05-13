# GraphQL
import graphene

# Schemas
from .notes import schema as schema_notes


class Query(
    schema_notes.Query, graphene.ObjectType,
):
    pass


class Mutation(
    schema_notes.Mutation, graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
