from django.shortcuts import render
from django.views.generic import ListView
from .models import Producto

def index(request):
    return render(request, 'productos/index.html')

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
