from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import FacturaForm
from .models import DetalleFactura, Producto, Factura

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
            
            # Lógica para guardar los detalles de la factura
            productos_seleccionados = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            
            for producto_id, cantidad in zip(productos_seleccionados, cantidades):
                if producto_id and cantidad:
                    producto = Producto.objects.get(pk=producto_id)
                    cantidad = int(cantidad)
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        subtotal=producto.precio * cantidad
                    )
            
            return redirect(reverse('factura:lista_facturas'))
        
        # Si el formulario no es válido, renderiza de nuevo la página con los errores
        productos = Producto.objects.all()
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos
        })