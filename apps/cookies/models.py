from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel
from apps.translations.models import Translatable


class Cookie(BaseModel, Translatable):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Title"))
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    essential_functional_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("Essential and functional cookie description")
    )
    analytical_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("Analytical cookie description")
    )
    external_content_cookies_description = models.TextField(
        null=True, blank=True, verbose_name=_("External content cookie description")
    )

    class Meta:
        verbose_name = "Cookie"
        verbose_name_plural = "Cookie's"

    def __str__(self):
        return self.title

    class TranslatableMeta:
        fields = [
            "title",
            "message",
            "essential_functional_cookies_description",
            "analytical_cookies_description",
            "external_content_cookies_description",
        ]
