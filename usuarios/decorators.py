from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def rol_requerido(*roles):
    def decorador(vista):
        @login_required
        def envoltura(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador