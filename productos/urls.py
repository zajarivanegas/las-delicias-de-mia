from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_menu, name='lista_menu'),
]