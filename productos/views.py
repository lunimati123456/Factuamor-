from django.shortcuts import render
from django.views.generic import ListView
from .models import Producto

# La vista de inicio ahora buscará la plantilla en la nueva ubicación
def index(request):
    return render(request, 'index.html')

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

