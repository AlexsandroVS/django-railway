# api/views.py

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    Persona, Empleado, Cliente, Proveedor,
    Categoria, Producto, Factura, Venta, Pedido, DetallePedido
)
from .serializers import (
    PersonaSerializer, EmpleadoSerializer, ClienteSerializer, ProveedorSerializer,
    CategoriaSerializer, ProductoSerializer, FacturaSerializer,
    VentaSerializer, PedidoSerializer, DetallePedidoSerializer, UserSerializer
)
from api import serializers

class RegisterClienteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            return Response({"message": "Cliente creado correctamente!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"nombre": user.username})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria_id', None)
        receta_obligatoria = self.request.query_params.get('receta_obligatoria', None)

        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)

        if receta_obligatoria is not None:
            # Filtrar productos que son medicamentos y tienen receta obligatoria
            queryset = queryset.filter(categoria__subcategoria__receta_obligatoria=receta_obligatoria)

        return queryset


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

def landing_page(request):
    return render(request, 'landing.html')
