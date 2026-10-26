from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from .decorators import rol_requerido 
from .forms import CrearCocineroForm 

@rol_requerido('duena')
def gestion_personal(request):
    usuarios = Usuario.objects.all().order_by('rol', 'username')
    return render(request, 'usuarios/gestion_personal.html', {'usuarios': usuarios})

@rol_requerido('duena')
def crear_cocinero(request):
    if request.method == 'POST':
        form = CrearCocineroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.rol = Usuario.Rol.COCINERO
            usuario.save()
            messages.success(request, "Cocinero creado exitosamente.")
            return redirect('gestion_personal')
    else:
        form = CrearCocineroForm()
    
    return render(request, 'usuarios/crear_cocinero.html', {'form': form})

@rol_requerido('duena')
def cambiar_rol(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if usuario == request.user and nuevo_rol != Usuario.Rol.DUENA:
            messages.error(request, "No puedes quitarte a ti misma el rol de dueña.")
        else:
            usuario.rol = nuevo_rol
            usuario.save()
            messages.success(request, f"Rol de {usuario.username} actualizado a {usuario.get_rol_display()}.")
    return redirect('gestion_personal')

@rol_requerido('duena')
def desactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if usuario != request.user:
        usuario.is_active = False 
        usuario.save()
        messages.warning(request, f"La cuenta de {usuario.username} ha sido desactivada correctamente.")
    else:
        messages.error(request, "No puedes desactivar tu propia cuenta.")
    return redirect('gestion_personal')