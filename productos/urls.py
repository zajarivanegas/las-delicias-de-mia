from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.gestion_menu, name='gestion_menu'),
    path('menu/producto/crear/', views.crear_producto, name='crear_producto'),
    path('menu/producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('menu/producto/agotar/<int:producto_id>/', views.toggle_agotado, name='toggle_agotado'),
    path('menu/producto/desactivar/<int:producto_id>/', views.desactivar_producto, name='desactivar_producto'),
    path('menu/categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('menu/categoria/desactivar/<int:categoria_id>/', views.desactivar_categoria, name='desactivar_categoria'),
]