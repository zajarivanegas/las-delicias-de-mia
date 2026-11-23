from django.shortcuts import render, get_object_or_404
from .models import Categoria, Producto

def lista_menu(request):
    # Solo traemos las categorías que estén activas
    categorias = Categoria.objects.filter(activa=True)

    # Revisamos si el usuario hizo clic en alguna categoría
    categoria_id = request.GET.get('categoria')
    categoria_actual = None

    if categoria_id:
        categoria_actual = get_object_or_404(Categoria, id=categoria_id, activa=True)
        productos = Producto.objects.filter(categoria=categoria_actual, disponible=True)
    else:
        # Si no eligió ninguna, mostramos todos los productos de categorías activas
        productos = Producto.objects.filter(categoria__activa=True, disponible=True)

    return render(request, 'productos/menu.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_actual': categoria_actual,
    })

# Create your views here.
