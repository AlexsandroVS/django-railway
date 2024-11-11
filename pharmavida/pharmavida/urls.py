from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView  # Importa TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import landing_page

# Configuración de Swagger para la documentación de la API
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API for managing products, sales, inventory, and more.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Página de inicio de la API
    path('admin/', admin.site.urls),  # Rutas de administración
    path('api/', include('api.urls')),  # Incluye las URLs de la API
    path('api-auth/', include('rest_framework.urls')),  # Rutas de autenticación de DRF
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar token JWT
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verificar token JWT
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Ruta para Swagger
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Ruta para archivos media
