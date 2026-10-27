from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('', RedirectView.as_view(pattern_name='login')),
    path('menu/', include('productos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
