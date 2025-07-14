from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from users.views import (
    LoginAPIview, 
    PasswordChangeAPIview
    )

# swagger ui schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation powered by Swagger",
        terms_of_service="https://your-terms-of-service-url.com/",
        contact=openapi.Contact(email="contact@your-api.com"),
        license=openapi.License(name="Your API License"),
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/',LoginAPIview.as_view(),name='login'),
    path('pswrd-change/<uuid:uuid>',PasswordChangeAPIview.as_view(),name='password-change'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # apps
    path('users/',include('users.urls')),
    path('schools/',include('schools.urls')),

    #JWT
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    #swagger
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]+static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )
