from django.contrib import admin
from .models import Producto,Cliente,Categoria,DetallePedido,Empleado,Factura,Pedido,Persona,Proveedor,Venta
# Register your models here

admin.site.register(Venta)
admin.site.register(Empleado)
admin.site.register(Factura)
admin.site.register(Pedido)
admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(DetallePedido)
admin.site.register(Producto)
admin.site.register(Persona)
