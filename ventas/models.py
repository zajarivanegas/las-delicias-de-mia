from django.db import models
from pedidos.models import Pedido
from productos.models import Producto

class Venta(models.Model):
    TIPO_CHOICES = (
        ('mesa', 'Mesa'), 
        ('domicilio', 'Domicilio')
    )
    
    PAGO_CHOICES = (
        ('efectivo', 'Efectivo'), 
        ('tarjeta', 'Tarjeta'), 
        ('transferencia', 'Transferencia')
    )

    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT, related_name='venta')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=PAGO_CHOICES, default='efectivo')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='mesa')

    def __str__(self):
        return f"Venta #{self.id} - Pedido #{self.pedido.id}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"