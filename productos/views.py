from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Producto

# Vista de catálogo público, página de inicio del sitio (sin autenticación ni permisos)
class CatalogoListView(ListView):
    model = Producto
    template_name = 'productos/catalogo_list.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        """ Filtra los productos para mostrar solo los que tienen stock disponible. """
        return Producto.objects.filter(stock__gt=0)
    
# Vista para ver los detalles de un solo producto (público, sin stock)
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

# Vista de gestión de productos (requiere autenticación y permisos)
class ProductoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
    permission_required = 'productos.view_producto'

# Vista para crear un nuevo producto (requiere autenticación y permisos)
class ProductoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:lista_productos')
    permission_required = 'productos.add_producto'
    
# Vista para editar un producto existente (requiere autenticación y permisos)
class ProductoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:lista_productos')
    permission_required = 'productos.change_producto'

# Vista para eliminar un producto (requiere autenticación y permisos)
class ProductoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('productos:lista_productos')
    permission_required = 'productos.delete_producto'