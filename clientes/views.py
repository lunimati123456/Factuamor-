from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente

# Vista para la lista de clientes
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'

# Vista para crear nuevos clientes
class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:lista_clientes')

# Vista para observar el detalle completo de un cliente
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'

# Vista para actualizar los datos del cliente
class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:lista_clientes')

# Vista para eliminar clientes
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista_clientes')
