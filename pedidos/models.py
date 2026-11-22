from django.contrib.auth.models import User
from django.db import models
from productos.models import Producto


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Pedido(models.Model):
    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("transferencia", "Transferencia"),
        ("otro", "Otro"),
    ]

    TIPOS_PEDIDO = [
        ("mesa", "En mesa"),
        ("domicilio", "Domicilio"),
    ]

    ESTADOS_PEDIDO = [
        ("pendiente", "Pendiente"),
        ("en_preparacion", "En preparación"),
        ("entregado", "Entregado"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    tipo_pedido = models.CharField(max_length=20, choices=TIPOS_PEDIDO, default="mesa")
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos")
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default="pendiente")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_tipo_pedido_display()} - {self.get_estado_display()}"



class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class ConfiguracionNegocio(models.Model):
    whatsapp_numero = models.CharField(
        max_length=20,
        blank=True,
        help_text="Número con código de país, sin + ni espacios. Ej: 573001234567",
    )

    def __str__(self):
        return f"WhatsApp negocio: {self.whatsapp_numero or 'No configurado'}"