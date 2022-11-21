from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from graphene_file_upload.django import FileUploadGraphQLView
from graphql_playground.views import GraphQLPlaygroundView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path(
        "graphql/",
        FileUploadGraphQLView.as_view(graphiql=True),
    ),
    path("playground/", GraphQLPlaygroundView.as_view(endpoint="/graphql/")),
    path("martor/", include("martor.urls")),
]


admin.site.site_header = "{app_name}"
admin.site.site_title = "{app_name} Admin Portal"
admin.site.index_title = "{app_name} Admin"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
    except ImportError:
        pass
