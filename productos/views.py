from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto

# La vista de inicio
def index(request):
    return render(request, 'index.html')

# Vista para la lista de productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

# Vista para crear un nuevo producto
class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:lista_productos')
    
# Vista para editar un producto existente
class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:lista_productos')

# Vista para eliminar un producto
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('productos:lista_productos')