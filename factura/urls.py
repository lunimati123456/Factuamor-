from django.urls import path
from .views import FacturaCreateView, FacturaDeleteView, FacturaListView, FacturaDetailView, FacturaUpdateView

app_name = 'factura'

urlpatterns = [
    path('crear/', FacturaCreateView.as_view(), name='crear_factura'),
    path('lista/', FacturaListView.as_view(), name='lista_facturas'),
    path('<int:pk>/', FacturaDetailView.as_view(), name='detalle_factura'),
    path('editar/<int:pk>/', FacturaUpdateView.as_view(), name='editar_factura'),
    path('eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='eliminar_factura'),
]