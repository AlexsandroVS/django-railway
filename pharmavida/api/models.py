from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Cambiar el método de default_user para devolver un ID de User, no un objeto
def get_default_user():
    user, created = User.objects.get_or_create(username='defaultuser', email='defaultuser@example.com')
    return user.id  # Devuelve solo el ID

# Función para crear una persona por defecto si no existe
def get_default_persona():
    persona, created = Persona.objects.get_or_create(
        nombre="Persona por Defecto",
        apellidos="Apellido por Defecto",
        correo="persona@example.com",
        telefono="0000000000",
        direccion="Dirección por defecto",
        identificacion="0000"
    )
    return persona.id  # Devuelve solo el ID

# Función para obtener un empleado por defecto
def get_default_empleado():
    empleado = Empleado.objects.first()  # O alguna lógica para obtener un empleado predeterminado.
    return empleado.id if empleado else None  # Devuelve solo el ID o None si no hay empleado

# Función para obtener un cliente por defecto
def get_default_cliente():
    cliente = Cliente.objects.first()  # O alguna lógica para obtener un cliente predeterminado.
    return cliente.id if cliente else None  # Devuelve solo el ID o None si no hay cliente

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    identificacion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Empleado(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, default=get_default_persona)
    cargo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    rol = models.CharField(
        max_length=10,
        choices=[('admin', 'Administrador'), ('empleado', 'Empleado')],
        default='empleado'
    )

    def __str__(self):
        return self.persona.nombre

class Cliente(models.Model):
    # Usando el ID del usuario por defecto
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=get_default_user)
    fecha_registro = models.DateField(default=timezone.now)
    direccion_envio = models.CharField(max_length=200, blank=True, null=True)
    telefono_secundario = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    # Subcategoría para medicamentos
    es_medicamento = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    presentacion = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', default='default_image.jpg')
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receta_obligatoria = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.categoria.es_medicamento and self.receta_obligatoria not in [True, False]:
            raise ValidationError('Si la categoría es medicamento, debe indicar si tiene receta obligatoria.')

class Factura(models.Model):
    cantidad = models.IntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, default=get_default_empleado)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=get_default_cliente)
    fecha = models.DateField()

class Venta(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Pedido(models.Model):
    fecha_pedido = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default=1)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=7, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_compra
        super().save(*args, **kwargs)
