from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name="registro"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('inicio/', views.inicio, name="inicio"),
    path('cocina/', views.cocina, name="cocina"),
    path('panel/', views.panel_admin, name="panel_admin"),
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/crear/', views.crear_cocinero, name='crear_cocinero'),
    path('personal/cambiar-rol/<int:usuario_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('personal/desactivar/<int:usuario_id>/', views.desactivar_usuario, name='desactivar_usuario'),
]