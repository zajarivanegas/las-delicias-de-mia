from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="categorias/", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True, verbose_name="Disponible en el menú")
    is_agotado = models.BooleanField(default=False, verbose_name="Agotado")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre