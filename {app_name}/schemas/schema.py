from graphene import ObjectType, Schema

from apps.blog.schemas.schema import Query as BlogQuery
from apps.contact.schemas.schema import Mutation as ContactMutation
from apps.cookies.schemas.schema import Query as CookieQuery
from apps.users.schemas.schema import Mutation as UserMutation
from apps.users.schemas.schema import Query as UserQuery


class Query(
    BlogQuery,
    CookieQuery,
    UserQuery,
    ObjectType,
):
    pass


class Mutation(ContactMutation, UserMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
