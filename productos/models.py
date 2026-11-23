from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, default="")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def precio_formateado(self):
        return f"${int(self.precio):,}".replace(",", ".")

    def __str__(self):
        return f"{self.nombre} ({self.precio_formateado()})"