from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from clientes.models import Cliente
from productos.models import Producto
from factura.models import Factura, DetalleFactura

class FacturaTests(TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test: crea un cliente y un producto."""
        self.cliente = Cliente.objects.create(nombre="Pepito Pérez")
        self.producto = Producto.objects.create(
            nombre="Camiseta",
            precio=100,
            stock=10
        )
        self.factura = Factura.objects.create(cliente=self.cliente)

    def test_crear_detalle_factura_descontando_stock(self):
        """Al crear un detalle, el stock del producto debe reducirse."""
        DetalleFactura.objects.create(
            factura=self.factura,
            producto=self.producto,
            cantidad=3
        )
        self.producto.refresh_from_db()
        self.factura.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)
        self.assertEqual(self.factura.total, 300)

    def test_no_permite_cantidad_mayor_a_stock(self):
        """Debe lanzar error si intentamos vender más stock del disponible."""
        with self.assertRaises(ValidationError):
            detalle = DetalleFactura(
                factura=self.factura,
                producto=self.producto,
                cantidad=20
            )
            detalle.full_clean()  # dispara las validaciones de clean()

    def test_eliminar_detalle_restaura_stock(self):
        """Si se elimina un detalle, el stock debe restaurarse."""
        detalle = DetalleFactura.objects.create(
            factura=self.factura,
            producto=self.producto,
            cantidad=4
        )
        detalle.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        
    def test_no_permite_producto_duplicado_en_factura(self):
        """No debe permitir que el mismo producto se añada dos veces a la misma factura."""
        DetalleFactura.objects.create(
            factura=self.factura,
            producto=self.producto,
            cantidad=1
        )
        with self.assertRaises(ValidationError):
            DetalleFactura.objects.create(
                factura=self.factura,
                producto=self.producto,
                cantidad=1
            )