from django.urls import path
from .views import ProductoListView

urlpatterns = [
    path('lista/', ProductoListView.as_view(), name='lista_productos'),
]