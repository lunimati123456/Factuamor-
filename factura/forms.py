from django import forms
from django.forms import inlineformset_factory
from .models import Factura, DetalleFactura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente']
        
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad']

# Usamos formset_factory para manejar múltiples DetalleFactura en un solo formulario
# Extra_forms=0 significa que no se añadirán formularios vacíos por defecto
# can_delete=True permite que el usuario marque un detalle para su eliminación
DetalleFacturaFormSet = inlineformset_factory(
    Factura, 
    DetalleFactura, 
    form=DetalleFacturaForm,
    fields=['producto', 'cantidad'],
    extra=0,
    can_delete=True
)
