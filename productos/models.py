from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    imagen = models.ImageField(upload_to="categorias/", blank=True)
    activa = models.BooleanField(default=True)   # False = no aparece en el menú
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="productos"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)  # pesos, sin decimales
    imagen = models.ImageField(upload_to="productos/", blank=True)
    disponible = models.BooleanField(default=True)  # False = "Agotado"

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre