from django.urls import path
from .views import FacturaCreateView, FacturaListView, FacturaDetailView

app_name = 'factura'

urlpatterns = [
    path('crear/', FacturaCreateView.as_view(), name='crear_factura'),
    path('lista/', FacturaListView.as_view(), name='lista_facturas'),
    path('<int:pk>/', FacturaDetailView.as_view(), name='detalle_factura'),
]