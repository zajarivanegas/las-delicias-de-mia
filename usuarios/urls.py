from django.urls import path
from . import views

urlpatterns = [
    path("registro/", views.registro_cliente, name="registro_cliente"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("menu/", views.vista_menu, name="menu"),
    path("cocina/", views.vista_cocina, name="cocina"),
    path("admin-panel/", views.vista_panel_admin, name="panel_admin"),
]