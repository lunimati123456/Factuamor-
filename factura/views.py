from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from .forms import FacturaForm
from .models import DetalleFactura, Producto, Factura
from decimal import Decimal

class FacturaCreateView(View):
    def get(self, request, *args, **kwargs):
        form = FacturaForm()
        productos = Producto.objects.all()
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos
        })

    def post(self, request, *args, **kwargs):
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.save()
            
            # Guardar los detalles de la factura
            productos_seleccionados = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            
            for producto_id, cantidad in zip(productos_seleccionados, cantidades):
                if producto_id and cantidad:
                    producto = Producto.objects.get(pk=producto_id)
                    cantidad = int(cantidad)
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad
                    )
            
            return redirect(reverse_lazy('factura:lista_facturas'))
        
        # Si el formulario no es válido, renderiza de nuevo la página con los errores
        productos = Producto.objects.all()
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos
        })


class FacturaListView(ListView):
    model = Factura
    template_name = 'factura/factura_list.html'
    context_object_name = 'facturas'
    ordering = ['-fecha']