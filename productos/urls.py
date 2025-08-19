from django.urls import path
from .views import ProductoListView, ProductoCreateView

app_name = 'productos'

urlpatterns = [
    path('lista/', ProductoListView.as_view(), name='lista_productos'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
]