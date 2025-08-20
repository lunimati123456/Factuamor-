from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView, ProductoDetailView

app_name = 'productos'

urlpatterns = [
    path('lista/', ProductoListView.as_view(), name='lista_productos'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
    path('detalle/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),
]