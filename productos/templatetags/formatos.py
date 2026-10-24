from django import template

register = template.Library()


@register.filter
def pesos(valor):
    """Convierte 12000 en $12.000"""
    try:
        entero = int(valor)
    except (TypeError, ValueError):
        return valor
    return "$" + f"{entero:,}".replace(",", ".")