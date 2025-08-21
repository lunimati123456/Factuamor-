from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteDetailView, ClienteUpdateView

app_name = 'clientes'

urlpatterns = [
    path('', ClienteListView.as_view(), name='lista_clientes'),
    path('crear/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('detalle/<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
]