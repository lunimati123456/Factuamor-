from django.views.generic import ListView, CreateView
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

