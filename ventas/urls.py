from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('reporte/', views.reporte_ventas, name='reporte_ventas'),
    path('mas-vendidos/', views.reporte_mas_vendidos, name='reporte_mas_vendidos'),
]