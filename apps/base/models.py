import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

import apps.base.constants as C


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Unique identification"),
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of creation"))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("Date of last update"))
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_("Delete date"))

    class Meta:
        abstract = True


class SortableModel(models.Model):
    position = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ["-position"]


class StateModel(models.Model):
    state = models.CharField(max_length=255, choices=C.STATES, default=C.STATE_DRAFT)

    class Meta:
        abstract = True

    def is_visible(self):
        return True if self.state == C.STATE_PUBLISHED else False


class SeoModel(models.Model):
    meta_title = models.CharField(
        null=True, max_length=55, blank=True, db_index=True, verbose_name=_("Meta title")
    )
    meta_keywords = models.TextField(
        null=True, max_length=255, blank=True, verbose_name=_("Meta keywords")
    )
    meta_description = models.TextField(null=True, blank=True, verbose_name=_("Meta description"))
    meta_image = models.CharField(
        null=True, blank=True, max_length=255, verbose_name=_("Meta image")
    )
    markup_data = models.TextField(null=True, blank=True, verbose_name=_("Structured markup data"))

    class Meta:
        abstract = True
