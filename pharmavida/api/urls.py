from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PersonaViewSet, EmpleadoViewSet, ClienteViewSet, ProveedorViewSet, 
    CategoriaViewSet, ProductoViewSet, RegisterView,
    FacturaViewSet, VentaViewSet, PedidoViewSet, DetallePedidoViewSet, CurrentUserView, 
    RegisterClienteView  # Agregamos el RegisterClienteView
)

router = DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)  # La vista de productos ahora maneja los medicamentos
router.register(r'facturas', FacturaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),  # Rutas de la API con prefijo v1
    path('v1/register/', RegisterView.as_view(), name='register'),  # Ruta para registrar usuario
    path('v1/current-user/', CurrentUserView.as_view(), name='current_user'),  # Ruta para usuario actual
    path('v1/register_cliente/', RegisterClienteView.as_view(), name='register_cliente'),  # Ruta para registrar cliente
]
