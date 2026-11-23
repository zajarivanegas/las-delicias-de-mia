from decimal import Decimal
from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from productos.models import Producto
from .models import ConfiguracionNegocio, DetallePedido, Mesa, Pedido
from django.http import JsonResponse
from django.utils import timezone
from usuarios.views import requerir_rol


def _obtener_resumen_carrito(request):
    carrito = request.session.get("carrito", {})
    items = []
    total = Decimal("0.00")

    for prod_id_str, cantidad in list(carrito.items()):
        producto = Producto.objects.filter(id=prod_id_str, disponible=True).first()
        if not producto or cantidad <= 0:
            carrito.pop(prod_id_str, None)
            continue

        precio_unitario = producto.precio
        subtotal = precio_unitario * cantidad
        total += subtotal

        items.append({
            "producto": producto,
            "precio_unitario": precio_unitario,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

    request.session["carrito"] = carrito
    return items, total


@login_required(login_url="login")
def menu_productos(request):
    productos = Producto.objects.filter(disponible=True).order_by("nombre")
    items, total = _obtener_resumen_carrito(request)
    return render(request, "menu.html", {
        "productos": productos,
        "items_carrito": items,
        "total_carrito": total,
    })


@login_required(login_url="login")
def agregar_al_carrito(request, producto_id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=producto_id, disponible=True)
        carrito = request.session.get("carrito", {})
        clave = str(producto.id)
        carrito[clave] = carrito.get(clave, 0) + 1
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, f"Se agregó '{producto.nombre}' al carrito.")
    return redirect("menu_productos")


@login_required(login_url="login")
def cambiar_cantidad(request, producto_id, accion):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})
        clave = str(producto_id)
        if clave in carrito:
            if accion == "sumar":
                carrito[clave] += 1
            elif accion == "restar":
                carrito[clave] -= 1
                if carrito[clave] <= 0:
                    carrito.pop(clave)
            elif accion == "eliminar":
                carrito.pop(clave)
            request.session["carrito"] = carrito
            request.session.modified = True
    return redirect("ver_carrito")

def _construir_url_whatsapp(items, total, numero_raw):
    if not items or not numero_raw:
        return None

    numero_limpio = "".join(ch for ch in str(numero_raw) if ch.isdigit())
    if not numero_limpio:
        return None

    lineas = ["Hola, quiero hacer un pedido a domicilio:", ""]
    for item in items:
        lineas.append(f"- {item['cantidad']} x {item['producto'].nombre} (${item['subtotal']})")
    lineas.append("")
    lineas.append(f"Total: ${total}")

    mensaje = quote("\n".join(lineas))
    return f"https://wa.me/{numero_limpio}?text={mensaje}"

@login_required(login_url="login")
def ver_carrito(request):
    items, total = _obtener_resumen_carrito(request)
    config = ConfiguracionNegocio.objects.first()
    whatsapp_url = _construir_url_whatsapp(items, total, config.whatsapp_numero if config else "")

    return render(request, "carrito.html", {
        "items_carrito": items,
        "total_carrito": total,
        "metodos_pago": Pedido.METODOS_PAGO,
        "tipos_pedido": Pedido.TIPOS_PEDIDO,
        "mesas": Mesa.objects.filter(activa=True).order_by("numero"),
        "whatsapp_url": whatsapp_url,
    })


@login_required(login_url="login")
def confirmar_pedido(request):
    if request.method != "POST":
        return redirect("ver_carrito")

    items, total = _obtener_resumen_carrito(request)
    if not items:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de confirmar.")
        return redirect("ver_carrito")

    metodo_pago = request.POST.get("metodo_pago", "").strip()
    metodos_validos = dict(Pedido.METODOS_PAGO)
    if metodo_pago not in metodos_validos:
        messages.error(request, "Debes elegir un método de pago: efectivo, transferencia u otro.")
        return redirect("ver_carrito")

    tipo_pedido = request.POST.get("tipo_pedido", "").strip()
    tipos_validos = dict(Pedido.TIPOS_PEDIDO)
    if tipo_pedido not in tipos_validos:
        messages.error(request, "Debes elegir el tipo de pedido: En mesa o Domicilio.")
        return redirect("ver_carrito")

    mesa_obj = None
    if tipo_pedido == "mesa":
        numero_mesa_raw = request.POST.get("numero_mesa", "").strip()
        if not numero_mesa_raw:
            messages.error(request, "Si eliges 'En mesa', debes indicar el número de mesa.")
            return redirect("ver_carrito")

        try:
            numero_mesa = int(numero_mesa_raw)
        except ValueError:
            messages.error(request, "El número de mesa no es válido.")
            return redirect("ver_carrito")

        mesa_obj = Mesa.objects.filter(numero=numero_mesa, activa=True).first()
        if not mesa_obj:
            messages.error(request, f"La mesa #{numero_mesa} no existe o no está disponible en el local.")
            return redirect("ver_carrito")

    pedido = Pedido.objects.create(
        cliente=request.user,
        tipo_pedido=tipo_pedido,
        mesa=mesa_obj,
        estado="pendiente",
        metodo_pago=metodo_pago,
        total=total,
    )

    resumen_partes = []
    for item in items:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item["producto"],
            precio_unitario=item["precio_unitario"],
            cantidad=item["cantidad"],
            subtotal=item["subtotal"],
        )
        resumen_partes.append(f"{item['cantidad']}x {item['producto'].nombre} (${item['subtotal']})")

    request.session["carrito"] = {}
    request.session.modified = True

    destino_texto = f"En mesa #{mesa_obj.numero}" if mesa_obj else "Domicilio"
    resumen_texto = ", ".join(resumen_partes)

    messages.success(
        request,
        f"Pedido #{pedido.id} confirmado ({destino_texto}, estado: Pendiente). "
        f"Resumen: {resumen_texto}. Total: ${pedido.total}."
    )
    return redirect("menu_productos")

@login_required(login_url="login")
@requerir_rol(["cocinero", "duena"])
def api_pedidos_cocina(request):
    # Solo pedidos activos (excluye los entregados), del más antiguo al más reciente
    pedidos = (
        Pedido.objects.exclude(estado="entregado")
        .select_related("mesa", "cliente")
        .prefetch_related("detalles__producto")
        .order_by("creado_en")
    )

    datos = []
    for pedido in pedidos:
        hora_local = timezone.localtime(pedido.creado_en).strftime("%I:%M %p")
        datos.append({
            "id": pedido.id,
            "tipo_pedido": pedido.get_tipo_pedido_display(),
            "mesa": pedido.mesa.numero if pedido.mesa else None,
            "estado": pedido.estado,
            "estado_display": pedido.get_estado_display(),
            "hora": hora_local,
            "detalles": [
                {
                    "cantidad": d.cantidad,
                    "producto": d.producto.nombre,
                }
                for d in pedido.detalles.all()
            ],
        })

    return JsonResponse({"pedidos": datos})
