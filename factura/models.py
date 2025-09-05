from django.db import models, transaction
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
        """Validación de stock y unicidad antes de guardar."""
        # Validar duplicidad (creación y edición)
        qs = DetalleFactura.objects.filter(factura=self.factura, producto=self.producto)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Este producto ya está en la factura.")

        # Validación de stock
        producto_actual = Producto.objects.get(pk=self.producto.pk)

        if self.pk:
            detalle_antiguo = DetalleFactura.objects.get(pk=self.pk)

            if detalle_antiguo.producto.pk == self.producto.pk:
                # mismo producto → stock disponible = stock actual + cantidad antigua
                disponible = producto_actual.stock + detalle_antiguo.cantidad
            else:
                # producto distinto → solo stock actual del nuevo producto
                disponible = producto_actual.stock
        else:
            disponible = producto_actual.stock

        if self.cantidad > disponible:
            raise ValidationError(
                f"Stock insuficiente para {self.producto.nombre}. "
                f"Disponible: {disponible}, Solicitado: {self.cantidad}"
            )
    
    def save(self, *args, **kwargs):
        self.clean()

        with transaction.atomic():
            if not self.pk:
                # Creación
                self.precio_unitario = self.producto.precio
                self.subtotal = self.cantidad * self.precio_unitario
                self.producto.stock -= self.cantidad
                self.producto.save()
            else:
                # Edición
                detalle_antiguo = DetalleFactura.objects.get(pk=self.pk)

                if detalle_antiguo.producto.pk != self.producto.pk:
                    # Cambió de producto
                    # Devolver stock al antiguo
                    prod_antiguo = detalle_antiguo.producto
                    prod_antiguo.stock += detalle_antiguo.cantidad
                    prod_antiguo.save()

                    # Actualizar precio unitario del nuevo producto
                    self.precio_unitario = self.producto.precio

                    # Descontar del nuevo producto
                    self.producto.stock -= self.cantidad
                    self.producto.save()
                else:
                    # Mismo producto → ajustar diferencia
                    diferencia = self.cantidad - detalle_antiguo.cantidad
                    if diferencia != 0:
                        self.producto.stock -= diferencia
                        self.producto.save()

                # Recalcular subtotal
                self.subtotal = self.cantidad * self.precio_unitario

            super().save(*args, **kwargs)

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