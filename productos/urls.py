from django.urls import path
from .views import (
    CatalogoListView,
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView,
    ProductoDetailView
)

app_name = 'productos'

urlpatterns = [
    # URLs para el catálogo público
    path('', CatalogoListView.as_view(), name='catalogo_productos'),
    path('detalle/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),

    # URLs para la gestión interna
    path('gestion/', ProductoListView.as_view(), name='lista_productos'),
    path('gestion/crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('gestion/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('gestion/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
]