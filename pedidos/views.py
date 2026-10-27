from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Pedido, HistorialEstado
from usuarios.decorators import rol_requerido

@rol_requerido('cocinero')
def lista_cocina(request):
    pedidos_activos = Pedido.objects.exclude(estado='entregado').order_by('fecha_creacion')
    return render(request, 'pedidos/cocina.html', {'pedidos': pedidos_activos})

@rol_requerido('cocinero')
def avanzar_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    orden_estados = ['pendiente', 'preparacion', 'listo', 'entregado']
    estado_actual_index = orden_estados.index(pedido.estado)
    
    if estado_actual_index < len(orden_estados) - 1:
        nuevo_estado = orden_estados[estado_actual_index + 1]
        pedido.estado = nuevo_estado
        pedido.save()
        
        HistorialEstado.objects.create(pedido=pedido, estado=nuevo_estado)
        messages.success(request, f"Pedido #{pedido.id} ahora está: {pedido.get_estado_display()}")
    else:
        messages.warning(request, "El pedido ya fue entregado.")

    return redirect('lista_cocina')

def estado_pedido_cliente(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    historial = pedido.historial.all()
    return render(request, 'pedidos/estado_cliente.html', {
        'pedido': pedido,
        'historial': historial
    })