from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Pedido, HistorialEstado
from usuarios.decorators import rol_requerido
from ventas.models import Venta, DetalleVenta

@rol_requerido('cocinero', 'duena')
def lista_cocina(request):
    pedidos_activos = Pedido.objects.exclude(estado='entregado').prefetch_related('detalles__producto').order_by('fecha_creacion')
    return render(request, 'pedidos/cocina.html', {'pedidos': pedidos_activos})

@rol_requerido('cocinero', 'duena')
def avanzar_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    orden_estados = ['pendiente', 'preparacion', 'listo', 'entregado']
    estado_actual_index = orden_estados.index(pedido.estado)
    
    if estado_actual_index < len(orden_estados) - 1:
        nuevo_estado = orden_estados[estado_actual_index + 1]
        pedido.estado = nuevo_estado
        pedido.save()
        
        HistorialEstado.objects.create(pedido=pedido, estado=nuevo_estado)

        if nuevo_estado == 'entregado':
            if not Venta.objects.filter(pedido=pedido).exists():
                total = sum(detalle.producto.precio * detalle.cantidad for detalle in pedido.detalles.all())
                
                venta = Venta.objects.create(
                    pedido=pedido,
                    total=total,
                    metodo_pago='efectivo',
                    tipo='mesa'
                )
                
                for detalle_pedido in pedido.detalles.all():
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=detalle_pedido.producto,
                        cantidad=detalle_pedido.cantidad,
                        precio_unitario=detalle_pedido.producto.precio
                    )
                
                messages.success(request, f"✅ Pedido #{pedido.id} ENTREGADO.<br><br>💰 ¡Venta #{venta.id} generada con éxito!<br><a href='/ventas/detalle/{venta.id}/' class='inline-block mt-3 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded shadow'>👉 Ver Recibo de Venta</a>")
            else:
                messages.success(request, f"Pedido #{pedido.id} ahora está: {pedido.get_estado_display()}")
        else:
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

def avanzar_pedido_temporal(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    orden_estados = ['pendiente', 'preparacion', 'listo', 'entregado']
    
    try:
        estado_actual_index = orden_estados.index(pedido.estado)
        if estado_actual_index < len(orden_estados) - 1:
            nuevo_estado = orden_estados[estado_actual_index + 1]
            pedido.estado = nuevo_estado
            pedido.save()
            HistorialEstado.objects.create(pedido=pedido, estado=nuevo_estado)
    except ValueError:
        pass 
        
    return redirect('lista_cocina')