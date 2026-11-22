from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    # Relacionamos con el usuario por defecto de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=20, default='cliente', editable=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"