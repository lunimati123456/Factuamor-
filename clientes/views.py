from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Cliente

# Vista para la lista de clientes (requiere estar logueado para ver)
class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    permission_required = 'clientes.view_cliente'

# Vista para crear nuevos clientes (requiere permisos de creación)
class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:lista_clientes')
    permission_required = 'clientes.add_cliente'

# Vista para observar el detalle completo de un cliente (requiere permisos para ver)
class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
    permission_required = 'clientes.view_cliente'

# Vista para actualizar los datos del cliente (requiere permisos de cambio)
class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:lista_clientes')
    permission_required = 'clientes.change_cliente'

# Vista para eliminar clientes (requiere permisos de eliminación)
class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista_clientes')
    permission_required = 'clientes.delete_cliente'