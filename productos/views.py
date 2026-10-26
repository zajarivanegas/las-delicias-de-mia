from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from usuarios.decorators import rol_requerido 

@rol_requerido('duena')
def gestion_menu(request):
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    categorias = Categoria.objects.all()
    return render(request, 'productos/gestion_menu.html', {'productos': productos, 'categorias': categorias})

@rol_requerido('duena')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('gestion_menu')
    else:
        form = ProductoForm()
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Crear Producto'})

@rol_requerido('duena')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect('gestion_menu')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Editar Producto'})

@rol_requerido('duena')
def toggle_agotado(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.is_agotado = not producto.is_agotado
    producto.save()
    messages.warning(request, f"Stock de {producto.nombre} actualizado.")
    return redirect('gestion_menu')

@rol_requerido('duena')
def desactivar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.is_active = False
    producto.save()
    messages.warning(request, f"Producto {producto.nombre} desactivado del menú.")
    return redirect('gestion_menu')

@rol_requerido('duena')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada.")
            return redirect('gestion_menu')
    else:
        form = CategoriaForm()
    return render(request, 'productos/form_categoria.html', {'form': form, 'titulo': 'Crear Categoría'})

@rol_requerido('duena')
def desactivar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.is_active = False
    categoria.save()
    messages.warning(request, f"Categoría {categoria.nombre} desactivada.")
    return redirect('gestion_menu')