from django.shortcuts import get_object_or_404, render

from .models import Categoria, Producto


def menu(request):
    # Criterio HU-03 (4): solo categorías activas
    categorias = Categoria.objects.filter(activa=True)
    productos = Producto.objects.filter(categoria__activa=True).select_related("categoria")

    # Criterio HU-03 (2): si eligió una categoría, solo sus productos
    categoria_actual = None
    categoria_id = request.GET.get("categoria")
    if categoria_id and categoria_id.isdigit():
        categoria_actual = get_object_or_404(categorias, pk=categoria_id)
        productos = productos.filter(categoria=categoria_actual)

    return render(request, "productos/menu.html", {
        "categorias": categorias,
        "productos": productos,
        "categoria_actual": categoria_actual,
    })