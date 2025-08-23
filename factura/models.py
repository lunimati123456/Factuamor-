from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
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
        self.save(update_fields=["total"])
    
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
    
    class Meta:
        unique_together = ("factura", "producto")
    
    def clean(self):
        """Validación de stock antes de guardar."""
        stock_actual = Producto.objects.get(pk=self.producto.pk).stock
        
        if not self.pk and self.cantidad > stock_actual:
            raise ValidationError(
                f"Stock insuficiente para {self.producto.nombre}. "
                f"Disponible: {stock_actual}, Solicitado: {self.cantidad}"
            )
        
        if self.pk:
            detalle_antiguo = DetalleFactura.objects.get(pk=self.pk)
            stock_disponible = stock_actual + detalle_antiguo.cantidad
            if self.cantidad > stock_disponible:
                raise ValidationError(
                    f"Stock insuficiente para {self.producto.nombre}. "
                    f"Disponible: {stock_disponible}, Solicitado: {self.cantidad}"
                )
    
    def save(self, *args, **kwargs):
        # 1. Validación previa
        self.clean()
        
        # 2. Proteger precio histórico
        if not self.pk:
            self.precio_unitario = self.producto.precio
        
        # 3. Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        
        # 4. Manejo de stock optimizado
        if self.pk:
            detalle_antiguo = DetalleFactura.objects.get(pk=self.pk)
            diferencia = self.cantidad - detalle_antiguo.cantidad
            
            if diferencia != 0:
                self.producto.stock -= diferencia
                self.producto.save()
        else:
            self.producto.stock -= self.cantidad
            self.producto.save()
        
        # 5. Guardar detalle
        super().save(*args, **kwargs)
        
        # 6. Actualizar total
        if not kwargs.get("raw", False):
            self.factura.actualizar_total()
    
    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Factura #{self.factura.pk}"

@receiver(post_delete, sender=DetalleFactura)
def devolver_stock_al_eliminar(sender, instance, **kwargs):
    """Devuelve el stock al eliminar un detalle."""
    instance.producto.stock += instance.cantidad
    instance.producto.save()
    instance.factura.actualizar_total()
