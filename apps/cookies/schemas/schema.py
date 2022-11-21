import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.utils import model_to_dict
from apps.cookies.models import Cookie


logger = logging.getLogger(__name__)


class CookieType(DjangoObjectType):
    class Meta:
        model = Cookie
        fields = "__all__"


class Query(graphene.ObjectType):
    get_cookie = graphene.Field(CookieType, lng=graphene.String())

    def resolve_get_cookie(self, info, lng: str = None):
        cookie = Cookie.objects.filter().first()
        logger.info(f"Get cookie: {model_to_dict(cookie)}")
        if lng:
            cookie = cookie.translate(lng)
            logger.info(f"Get translated cookie: {model_to_dict(cookie)}")
        return cookie
