from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SimplED API",
      default_version='v1',
      description="Good Luck, mobile developers :)",
      contact=openapi.Contact(email="roman.tarasov1@nure.ua"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui')
]
