from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import FacturaForm
from .models import DetalleFactura, Producto, Factura
from collections import defaultdict
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class FacturaCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'factura.add_factura'
    def get(self, request, *args, **kwargs):
        form = FacturaForm()
        productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos
        })

    def post(self, request, *args, **kwargs):
        form = FacturaForm(request.POST)
        
        if not form.is_valid():
            productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
            return render(request, 'factura/factura_form.html', {
                'form': form,
                'productos': productos
            })
        
        try:
            with transaction.atomic():
                factura = form.save()
                
                # Agrupar cantidades por producto
                productos_seleccionados = request.POST.getlist('producto')
                cantidades = request.POST.getlist('cantidad')
                
                productos_agrupados = defaultdict(int)
                for producto_id, cantidad in zip(productos_seleccionados, cantidades):
                    if producto_id and cantidad:
                        productos_agrupados[int(producto_id)] += int(cantidad)
                
                for producto_id, cantidad in productos_agrupados.items():
                    if cantidad <= 0:
                        raise ValidationError("La cantidad de un producto debe ser mayor a 0.")
                    
                    producto = Producto.objects.get(pk=producto_id)
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad
                    )
                
                return redirect(reverse_lazy('factura:lista_facturas'))
        
        except ValidationError as e:
            form.add_error(None, e)
        except Exception as e:
            form.add_error(None, f"Error inesperado: {str(e)}")
        
        productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos
        })

class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'factura/factura_list.html'
    context_object_name = 'facturas'
    ordering = ['-fecha']
    paginate_by = 10
    
class FacturaDetailView(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'factura/factura_detail.html'
    context_object_name = 'factura'

class FacturaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Factura
    template_name = 'factura/factura_confirm_delete.html'
    success_url = reverse_lazy('factura:lista_facturas')
    permission_required = 'factura.delete_factura'