from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroClienteForm
from .models import PerfilUsuario


def requerir_rol(roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para acceder.")
                return redirect("login")

            perfil = getattr(request.user, "perfil", None)
            if not perfil or perfil.rol not in roles_permitidos:
                messages.error(request, "Acceso denegado: no tienes permisos para esta vista.")
                if perfil and perfil.rol == "cocinero":
                    return redirect("cocina")
                if perfil and perfil.rol == "duena":
                    return redirect("panel_admin")
                return redirect("menu_productos") 

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorador


def redirigir_segun_rol(usuario):
    perfil = getattr(usuario, "perfil", None)
    rol = perfil.rol if perfil else "cliente"

    if rol == "cocinero":
        return redirect("cocina")
    if rol == "duena":
        return redirect("panel_admin")
    return redirect("menu_productos")


def registro_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            correo = form.cleaned_data["correo"]
            telefono = form.cleaned_data["telefono"]
            password = form.cleaned_data["password"]

            nuevo_usuario = User.objects.create_user(
                username=correo,
                email=correo,
                password=password,
                first_name=nombre,
            )

            PerfilUsuario.objects.create(
                usuario=nuevo_usuario,
                telefono=telefono,
                rol="cliente",
            )

            login(request, nuevo_usuario)
            messages.success(request, "¡Cuenta creada exitosamente! Bienvenido.")
            return redirect("menu_productos")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistroClienteForm()

    return render(request, "registro.html", {"form": form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirigir_segun_rol(request.user)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]

            usuario = authenticate(request, username=correo, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f"¡Hola de nuevo, {usuario.first_name}!")
                return redirigir_segun_rol(usuario)
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("login")


@login_required(login_url="login")
@requerir_rol(["cliente"])
def vista_menu(request):
    return render(request, "menu.html")

@login_required(login_url="login")
@requerir_rol(["cocinero", "duena"])
def vista_cocina(request):
    return render(request, "pedidos/cocina.html")


@login_required(login_url="login")
@requerir_rol(["duena"])
def vista_panel_admin(request):
    return render(request, "panel_admin.html")