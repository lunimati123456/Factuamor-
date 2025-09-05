# Importaciones de la biblioteca estándar
from collections import defaultdict

# Importaciones de Django (terceros)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView
from django_weasyprint import WeasyTemplateResponseMixin

# Importaciones locales
from .forms import FacturaForm, DetalleFacturaFormSet
from .models import Factura, DetalleFactura, Producto


class FacturaCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'factura.add_factura'
    
    def get(self, request, *args, **kwargs):
        form = FacturaForm()
        productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos,
            'is_update_view': False
        })

    def post(self, request, *args, **kwargs):
        form = FacturaForm(request.POST)
        
        if not form.is_valid():
            productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
            return render(request, 'factura/factura_form.html', {
                'form': form,
                'productos': productos,
                'is_update_view': False
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
                        
                if not productos_agrupados:
                    raise ValidationError("La factura debe contener al menos un producto.")
                
                for producto_id, cantidad in productos_agrupados.items():
                    if cantidad <= 0:
                        raise ValidationError("La cantidad de un producto debe ser mayor a 0.")
                    
                    producto = Producto.objects.get(pk=producto_id)
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad
                    )
                
                factura.actualizar_total()
                
                return redirect(reverse_lazy('factura:lista_facturas'))
        
        except ValidationError as e:
            form.add_error(None, e)
        except Exception as e:
            form.add_error(None, f"Error inesperado: {str(e)}")
        
        productos = Producto.objects.only('id', 'nombre', 'precio', 'stock')
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'productos': productos,
            'is_update_view': False
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

class FacturaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'factura.change_factura'

    def get(self, request, pk, *args, **kwargs):
        factura = get_object_or_404(Factura, pk=pk)
        form = FacturaForm(instance=factura)
        formset = DetalleFacturaFormSet(instance=factura, prefix='detalle')
        
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'formset': formset,
            'is_update_view': True,
            'factura': factura,
        })

    def post(self, request, pk, *args, **kwargs):
        factura = get_object_or_404(Factura, pk=pk)
        form = FacturaForm(request.POST, instance=factura)
        formset = DetalleFacturaFormSet(request.POST, instance=factura, prefix='detalle')

        if not form.is_valid() or not formset.is_valid():
            return render(request, 'factura/factura_form.html', {
                'form': form,
                'formset': formset,
                'is_update_view': True,
                'factura': factura,
            })

        try:
            with transaction.atomic():
                factura = form.save(commit=False)

                # Contar cuántos formularios no están marcados como eliminados
                non_deleted = [
                    f for f in formset
                    if f.cleaned_data and not f.cleaned_data.get('DELETE', False)
                ]
                if len(non_deleted) == 0:
                    raise ValidationError("La factura debe contener al menos un producto.")

                # Guardar detalles
                detalles = formset.save(commit=False)
                for d in detalles:
                    d.factura = factura
                    d.save()

                # Procesar eliminados
                for deleted in formset.deleted_objects:
                    deleted.delete()

                factura.actualizar_total()
                factura.save()

            return redirect(reverse_lazy('factura:lista_facturas'))
        
        except ValidationError as e:
            form.add_error(None, e)
        
        return render(request, 'factura/factura_form.html', {
            'form': form,
            'formset': formset,
            'is_update_view': True,
            'factura': factura,            
        })

# Vista para generar el PDF
class FacturaPDFView(LoginRequiredMixin, PermissionRequiredMixin, WeasyTemplateResponseMixin, DetailView):
    permission_required = 'factura.view_factura'
    model = Factura
    template_name = 'factura/factura_pdf.html'

    # Nombre dinámico del archivo PDF
    def get_pdf_filename(self):
        factura_id = self.get_object().pk
        return f'factura_{factura_id}.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factura'] = self.get_object()
        return context