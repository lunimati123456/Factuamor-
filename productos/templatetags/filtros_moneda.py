# C:\Users\PAULA\Desktop\Factuamor-\productos\templatetags\filtros_moneda.py
from django import template

register = template.Library()

@register.filter
def moneda_cop(value, mostrar_cop=False):
    """
    Formatea un valor numérico en pesos colombianos.
    Ej: 17000 -> $17.000
    Con mostrar_cop=True -> $17.000 COP
    """
    try:
        valor = int(value)
        texto = f"${valor:,}".replace(",", ".")
        return f"{texto} COP" if mostrar_cop else texto
    except (ValueError, TypeError):
        return value