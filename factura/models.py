from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from productos.models import Producto

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    def actualizar_total(self):
        """Recalcula el total sumando los subtotales de los detalles."""
        total = sum(detalle.subtotal for detalle in self.detallefactura_set.all())
        self.total = total
        self.save(update_fields=["total"])  # Evita recursión
    
    def __str__(self):
        return f"Factura #{self.pk} - {self.cliente}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(1)]
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(1)]
    )
    
    def save(self, *args, **kwargs):
        # Actualiza precio_unitario y subtotal
        self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        
        # Actualiza el total de la factura solo si es un detalle nuevo o modificado
        if not kwargs.get("raw", False):  # Evita recursión en cargas masivas
            self.factura.actualizar_total()
    
    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Factura #{self.factura.pk}"
