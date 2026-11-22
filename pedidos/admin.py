from django.contrib import admin
from .models import ConfiguracionNegocio, DetallePedido, Mesa, Pedido


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero", "activa")
    list_filter = ("activa",)


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "tipo_pedido", "mesa", "estado", "metodo_pago", "total", "creado_en")
    list_filter = ("tipo_pedido", "estado", "metodo_pago")
    inlines = [DetallePedidoInline]

@admin.register(ConfiguracionNegocio)
class ConfiguracionNegocioAdmin(admin.ModelAdmin):
    list_display = ("id", "whatsapp_numero")