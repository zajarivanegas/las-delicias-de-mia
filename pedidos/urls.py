from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu_productos, name="menu_productos"),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/<int:producto_id>/<str:accion>/", views.cambiar_cantidad, name="cambiar_cantidad"),
    path("carrito/confirmar/", views.confirmar_pedido, name="confirmar_pedido"),
]