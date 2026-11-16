import unittest

from enums.tipos import Estado, FormaPago, Rol
from excepciones.errores import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class FoodStorePruebas(unittest.TestCase):
    def setUp(self) -> None:
        self.categorias = CategoriaServicio()
        self.productos = ProductoServicio(self.categorias)
        self.usuarios = UsuarioServicio()
        self.pedidos = PedidoServicio(self.usuarios, self.productos)
        self.categoria = self.categorias.crear("Bebidas", "Bebidas frías")
        self.producto = self.productos.crear(
            nombre="Agua",
            precio=100.0,
            stock=5,
            id_categoria=self.categoria.id,
            descripcion="Agua mineral",
            imagen="agua.png",
            disponible=True,
        )
        self.usuario = self.usuarios.crear(
            nombre="Ana",
            apellido="Pérez",
            mail="ana@example.com",
            celular="1100000000",
            contrasenia="clave123",
            rol=Rol.USUARIO,
        )

    def test_categoria_rechaza_nombre_duplicado_sin_distinguir_mayusculas(self) -> None:
        with self.assertRaises(DuplicadoError):
            self.categorias.crear("BEBIDAS", "Otra descripción")

    def test_categoria_no_se_elimina_si_tiene_productos_activos(self) -> None:
        with self.assertRaises(OperacionNoPermitidaError):
            self.categorias.eliminar(
                self.categoria.id,
                self.productos.listar(),
            )

    def test_autenticacion_y_error_generico(self) -> None:
        usuario = self.usuarios.autenticar("ANA@example.com", "clave123")
        self.assertEqual(usuario.id, self.usuario.id)
        with self.assertRaises(CredencialesInvalidasError):
            self.usuarios.autenticar("ana@example.com", "incorrecta")

    def test_crear_pedido_acumula_detalle_y_descuenta_stock(self) -> None:
        pedido = self.pedidos.crear(
            self.usuario.id,
            FormaPago.EFECTIVO,
            [(self.producto.id, 2), (self.producto.id, 1)],
        )
        self.assertEqual(len(pedido.detalles), 1)
        self.assertEqual(pedido.detalles[0].cantidad, 3)
        self.assertEqual(pedido.total, 300.0)
        self.assertEqual(self.producto.stock, 2)

    def test_pedido_invalido_no_descuenta_stock_ni_se_guarda(self) -> None:
        with self.assertRaises(StockInsuficienteError):
            self.pedidos.crear(
                self.usuario.id,
                FormaPago.EFECTIVO,
                [(self.producto.id, 2), (self.producto.id, 4)],
            )
        self.assertEqual(self.producto.stock, 5)
        self.assertEqual(self.pedidos.listar(), [])

    def test_cancelar_devuelve_stock_una_sola_vez(self) -> None:
        pedido = self.pedidos.crear(
            self.usuario.id,
            FormaPago.EFECTIVO,
            [(self.producto.id, 2)],
        )
        self.pedidos.actualizar_estado(pedido.id, Estado.CANCELADO)
        self.assertEqual(self.producto.stock, 5)
        with self.assertRaises(OperacionNoPermitidaError):
            self.pedidos.actualizar_estado(pedido.id, Estado.CANCELADO)
        self.assertEqual(self.producto.stock, 5)

    def test_eliminar_pedido_pendiente_devuelve_stock_y_es_baja_logica(self) -> None:
        pedido = self.pedidos.crear(
            self.usuario.id,
            FormaPago.EFECTIVO,
            [(self.producto.id, 2)],
        )
        self.pedidos.eliminar(pedido.id)
        self.assertEqual(self.producto.stock, 5)
        self.assertEqual(self.pedidos.listar(), [])
        self.assertTrue(pedido.eliminado)
        self.assertTrue(pedido.detalles[0].eliminado)

    def test_cliente_no_puede_ver_pedido_ajeno(self) -> None:
        pedido = self.pedidos.crear(
            self.usuario.id,
            FormaPago.EFECTIVO,
            [(self.producto.id, 1)],
        )
        with self.assertRaises(EntidadNoEncontradaError):
            self.pedidos.buscar_para_usuario(pedido.id, self.usuario.id + 1)


if __name__ == "__main__":
    unittest.main()
