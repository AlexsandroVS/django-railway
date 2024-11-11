from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Persona, Empleado, Cliente, Proveedor,
    Categoria, Producto, Factura, Venta, Pedido, DetallePedido
)
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Asegúrate de que la contraseña no se muestre al leer

    def create(self, validated_data):
        user = User(**validated_data)  # Crea el usuario
        user.set_password(validated_data['password'])  # Asegúrate de guardar la contraseña de forma segura
        user.save()  # Guarda el usuario en la base de datos
        return user  # Retorna el usuario creado

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Empleado
        fields = '__all__'

    def create(self, validated_data):
        # Extrae los datos relacionados con Persona
        persona_data = validated_data.pop('persona')
        
        # Crea el objeto Persona
        persona_instance = Persona.objects.create(**persona_data)
        
        # Crea el objeto Empleado con la instancia de Persona
        empleado = Empleado.objects.create(persona=persona_instance, **validated_data)
        
        return empleado

class ClienteSerializer(serializers.ModelSerializer):
    # Campos relacionados del usuario
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Cliente
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        # Extrae los datos de usuario desde validated_data
        user_data = validated_data.pop('user')
        
        # Crear el usuario asociado al cliente
        user = User.objects.create_user(
            username=user_data['email'],  # Usa el correo como nombre de usuario
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=validated_data.pop('password')
        )
        
        # Crear el cliente y asociar el usuario creado
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)  
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    receta_obligatoria = serializers.BooleanField(write_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

    fecha_vencimiento = serializers.DateField(required=True)  # Asegurándote de que este campo esté bien definido

    def validate(self, data):
        categoria = data.get('categoria')  # Asegúrate de que 'categoria' esté obteniendo correctamente el objeto de 'Categoria'
        if categoria and not isinstance(categoria, Categoria):
            raise serializers.ValidationError("El campo categoria debe ser una instancia de Categoria.")
        return data
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'
