from django.contrib import admin
from django.db import models, transaction

from martor.widgets import AdminMartorWidget

from apps.base.utils import image_view
from apps.blog.models import Blog
from apps.translations.admin import TranslatableAdmin, TranslationInline
from apps.translations.tasks import translate_object


class BlogAdmin(TranslatableAdmin, admin.ModelAdmin):
    actions = ["make_published", "make_draft"]
    search_fields = ("name", "description")
    list_display = ("name", "date_created", "state", "image_tag")
    readonly_fields = ("image_preview",)
    list_editable = ("state",)
    fields = (
        "state",
        "name",
        "description",
        "image",
        "image_preview",
        "keywords",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )

    def image_preview(self, obj):
        return image_view(obj, 300, 300)

    def image_tag(self, obj):
        return image_view(obj, 100, 100)

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [
        TranslationInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("blog.Blog", obj.id))
        super().save_model(request, obj, form, change)


admin.site.register(Blog, BlogAdmin)
