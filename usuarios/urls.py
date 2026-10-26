from django.urls import path
from . import views

urlpatterns = [
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/crear/', views.crear_cocinero, name='crear_cocinero'),
    path('personal/cambiar-rol/<int:usuario_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('personal/desactivar/<int:usuario_id>/', views.desactivar_usuario, name='desactivar_usuario'),
]