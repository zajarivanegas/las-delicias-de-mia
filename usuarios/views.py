from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .decorators import rol_requerido
from .forms import LoginForm, RegistroClienteForm
from .models import Usuario


# ---------- HU-01: Registro de cliente ----------
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


# ---------- HU-02: Inicio y cierre de sesión ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.usuario)
            # Si venía de una página restringida, lo devolvemos allí
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


# Criterio 4: cada rol va a su vista
@login_required
def inicio(request):
    destinos = {
        Usuario.Rol.CLIENTE: "menu",
        Usuario.Rol.COCINERO: "cocina",
        Usuario.Rol.DUENA: "panel_admin",
    }
    return redirect(destinos.get(request.user.rol, "menu"))

#mientras gabi hace el de ella



@rol_requerido(Usuario.Rol.COCINERO)
def cocina(request):
    return render(request, "usuarios/pagina_rol.html", {"titulo": "Vista de cocina"})


@rol_requerido(Usuario.Rol.DUENA)
def panel_admin(request):
    return render(request, "usuarios/pagina_rol.html", {"titulo": "Panel de administración"})