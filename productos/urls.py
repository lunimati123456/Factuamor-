from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView

app_name = 'productos'

urlpatterns = [
    path('lista/', ProductoListView.as_view(), name='lista_productos'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
]