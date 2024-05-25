from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django Chat",
        default_version='1.0.0',
        description="A real time django chat application",
        terms_of_service="",
        contact=openapi.Contact(email="shresthasaurab030@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
api_prefix = 'api/v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix + 'users/', include('users.urls')),
]

# swagger docs
urlpatterns += [
    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=10),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    