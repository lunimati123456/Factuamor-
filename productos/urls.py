from django.urls import path
from .views import ProductoListView

app_name = 'productos'

urlpatterns = [
    path('lista/', ProductoListView.as_view(), name='lista_productos'),
]