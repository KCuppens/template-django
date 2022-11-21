from django.db import models

from apps.base.models import BaseModel
from apps.config.managers import ConfigManager


class Config(BaseModel):
    key_name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    value = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    objects = ConfigManager()

    def __str__(self):
        return self.title
