from django.urls import path
from . import views

urlpatterns = [
    path('cocina/', views.lista_cocina, name='lista_cocina'),
    path('cocina/avanzar/<int:pedido_id>/', views.avanzar_estado, name='avanzar_estado'),
    path('estado/<int:pedido_id>/', views.estado_pedido_cliente, name='estado_cliente'),
]