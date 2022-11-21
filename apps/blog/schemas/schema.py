import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.utils import model_to_dict, models_to_dict
from apps.blog.models import Blog


logger = logging.getLogger(__name__)


class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = "__all__"


class Query(graphene.ObjectType):
    get_filter_blogs = graphene.List(
        BlogType,
        name=graphene.String(),
        lng=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    get_blog_detail = graphene.Field(BlogType, id=graphene.String(), lng=graphene.String())

    def resolve_get_blog_detail(self, info, id, lng: str = None):
        blog = Blog.objects.filter(id=id).first()
        logger.info(f"Get blog detail: {model_to_dict(blog)}")
        if lng:
            blog = blog.translate(lng)
            logger.info(f"Get translated blog detail: {model_to_dict(blog)}")
        return blog

    def resolve_get_filter_blogs(
        self,
        info,
        name=None,
        lng: str = None,
        limit=25,
        offset=0,
    ):
        if name:
            blogs = Blog.objects.filter(name__icontains=name).order_by("-id")
            logger.info(f"Get blogs by name: {models_to_dict(blogs)}")
        if lng:
            blogs = blogs.translate(lng)
            logger.info(f"Get translated blogs: {models_to_dict(blogs)}")
        return blogs[offset : offset + limit]  # noqa E203
