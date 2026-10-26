from django.contrib import admin
from .models import Categoria, Producto

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "orden")
    list_editable = ("activa", "orden")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "disponible")
    list_filter = ("categoria", "disponible")
    list_editable = ("disponible",)
admin.site.register(Categoria)
admin.site.register(Producto)
