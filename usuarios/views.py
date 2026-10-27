from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.contrib import messages

from .decorators import rol_requerido
from .forms import LoginForm, RegistroClienteForm, CrearCocineroForm
from .models import Usuario


def registro(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.guardar()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = RegistroClienteForm()

    return render(request, "usuarios/registro.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.usuario)
            siguiente = request.GET.get("next")
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente, allowed_hosts={request.get_host()}
            ):
                return redirect(siguiente)
            return redirect("inicio")
    else:
        form = LoginForm()

    return render(request, "usuarios/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def inicio(request):
    destinos = {
        Usuario.Rol.CLIENTE: "menu",
        Usuario.Rol.COCINERO: "cocina",
        Usuario.Rol.DUENA: "panel_admin",
    }
    return redirect(destinos.get(request.user.rol, "menu"))


@rol_requerido(Usuario.Rol.COCINERO)
def cocina(request):
    return render(request, "usuarios/pagina_rol.html", {"titulo": "Vista de cocina"})


@rol_requerido(Usuario.Rol.DUENA)
def panel_admin(request):
    return render(request, "usuarios/pagina_rol.html", {"titulo": "Panel de administración"})


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