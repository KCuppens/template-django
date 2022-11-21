from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from apps.base.models import BaseModel, SeoModel, StateModel
from apps.translations.models import Translatable


class Blog(BaseModel, SeoModel, StateModel, Translatable):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from="name", unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to="blog/", verbose_name=_("Image"))
    keywords = models.TextField(blank=True, verbose_name=_("Keywords"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"
        ordering = ["-date_created"]

    class TranslatableMeta:
        fields = ["name", "description", "slug", "meta_title", "meta_description", "meta_keywords"]
