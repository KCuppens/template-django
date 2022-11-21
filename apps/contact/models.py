from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    first_name = models.CharField(
        max_length=25, verbose_name=_("First Name"), null=True, blank=True
    )
    last_name = models.CharField(max_length=25, verbose_name=_("Last Name"), null=True, blank=True)
    phone = models.CharField(max_length=25, verbose_name=_("Phone"), null=True, blank=True)
    message = models.TextField(verbose_name=_("Message"))
    email = models.EmailField(max_length=100, verbose_name=_("Email"), null=True, blank=True)
