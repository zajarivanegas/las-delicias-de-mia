from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    
    is_active = models.BooleanField(default=True, verbose_name="Disponible en el menú")
    is_agotado = models.BooleanField(default=False, verbose_name="Agotado")

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"