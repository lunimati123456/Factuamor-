from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción del Producto", blank=True, null=True)
    precio = models.IntegerField(verbose_name='Precio (COP)')
    stock = models.PositiveIntegerField(verbose_name="Stock disponible", default=0)
    imagen = models.ImageField(upload_to='productos/', verbose_name="Imagen del Producto", blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre