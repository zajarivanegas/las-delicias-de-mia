from django.shortcuts import render, get_object_or_404
from .models import Venta
from usuarios.decorators import rol_requerido
from datetime import datetime
from .models import Venta, DetalleVenta

@rol_requerido('duena')
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_hora')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

@rol_requerido('duena')
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'ventas/detalle_venta.html', {'venta': venta})
@rol_requerido('duena')
def reporte_ventas(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    ventas = Venta.objects.all().order_by('-fecha_hora')
    
    if fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            ventas = ventas.filter(fecha_hora__date__gte=inicio, fecha_hora__date__lte=fin)
        except ValueError:
            pass
            
    total_vendido = 0
    cantidad_ventas = ventas.count()
    
    pagos = {
        'efectivo': 0,
        'tarjeta': 0,
        'transferencia': 0
    }
    
    for v in ventas:
        total_vendido = total_vendido + v.total
        
        if v.metodo_pago == 'efectivo':
            pagos['efectivo'] = pagos['efectivo'] + v.total
        elif v.metodo_pago == 'tarjeta':
            pagos['tarjeta'] = pagos['tarjeta'] + v.total
        elif v.metodo_pago == 'transferencia':
            pagos['transferencia'] = pagos['transferencia'] + v.total
            
    contexto = {
        'ventas': ventas,
        'total_vendido': total_vendido,
        'cantidad_ventas': cantidad_ventas,
        'pagos': pagos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }
    
    return render(request, 'ventas/reporte_ventas.html', contexto)

@rol_requerido('duena')
def reporte_mas_vendidos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    detalles = DetalleVenta.objects.all()
    
    if fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            detalles = detalles.filter(venta__fecha_hora__date__gte=inicio, venta__fecha_hora__date__lte=fin)
        except ValueError:
            pass
            
    ranking = {}
    
    for detalle in detalles:
        nombre_prod = detalle.producto.nombre
        
        if nombre_prod not in ranking:
            ranking[nombre_prod] = {'cantidad': 0, 'ingreso': 0}
            
        ranking[nombre_prod]['cantidad'] = ranking[nombre_prod]['cantidad'] + detalle.cantidad
        ranking[nombre_prod]['ingreso'] = ranking[nombre_prod]['ingreso'] + (detalle.cantidad * detalle.precio_unitario)
        
    lista_ranking = []
    
    for nombre, datos in ranking.items():
        lista_ranking.append({
            'nombre': nombre,
            'cantidad': datos['cantidad'],
            'ingreso': datos['ingreso']
        })
        
    lista_ranking.sort(key=lambda x: x['cantidad'], reverse=True)
    
    contexto = {
        'ranking': lista_ranking,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'ventas/mas_vendidos.html', contexto)
