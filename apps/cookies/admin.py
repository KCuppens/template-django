from django.contrib import admin
from django.db import models, transaction

from martor.widgets import AdminMartorWidget

from apps.cookies.models import Cookie
from apps.translations.admin import TranslatableAdmin, TranslationInline
from apps.translations.tasks import translate_object


class CookieAdmin(TranslatableAdmin, admin.ModelAdmin):
    actions = ["make_published", "make_draft"]
    list_display = ("title",)
    fields = (
        "title",
        "message",
        "essential_functional_cookies_description",
        "analytical_cookies_description",
        "external_content_cookies_description",
    )

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [
        TranslationInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("cookies.Cookie", obj.id))
        super().save_model(request, obj, form, change)


admin.site.register(Cookie, CookieAdmin)
