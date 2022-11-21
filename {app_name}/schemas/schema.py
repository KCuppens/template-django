from graphene import ObjectType, Schema

from apps.blog.schemas.schema import Query as BlogQuery
from apps.contact.schemas.schema import Mutation as ContactMutation
from apps.cookies.schemas.schema import Query as CookieQuery
from apps.services.schemas.schema import Query as ServiceQuery
from apps.testimonials.schemas.schema import Query as TestimonialQuery
from apps.users.schemas.schema import Mutation as UserMutation
from apps.users.schemas.schema import Query as UserQuery
from apps.webshop.category.schemas.schema import Query as CategoryQuery
from apps.webshop.product.schemas.schema import Query as ProductQuery


class Query(
    ProductQuery,
    CategoryQuery,
    TestimonialQuery,
    BlogQuery,
    CookieQuery,
    ServiceQuery,
    UserQuery,
    ObjectType,
):
    pass


class Mutation(ContactMutation, UserMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
