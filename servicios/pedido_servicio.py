from entidades.pedido import Pedido
from enums.tipos import FormaPago,Estado
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from excepciones.errores import DatoInvalidoError, EntidadNoEncontradaError


class PedidoServicio:
    def __init__(self,usuario_servicio: UsuarioServicio,producto_servicio: ProductoServicio,) -> None:
        self.__pedidos: list[Pedido] = []
        self.__usuario_servicio: UsuarioServicio = usuario_servicio
        self.__producto_servicio: ProductoServicio = producto_servicio

    def listar(self) -> list[Pedido]:
        return [
            pedido for pedido in self.__pedidos
            if not pedido.eliminado
        ]

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido

        raise EntidadNoEncontradaError(
            f"No se encontró el pedido con id {id_pedido}"
        )

    def crear(self,id_usuario: int,forma_pago: FormaPago,detalles: list[tuple[int, int]],) -> Pedido:
        if not detalles:
            raise DatoInvalidoError("El pedido debe tener al menos un detalle")

        usuario = self.__usuario_servicio.buscar_por_id(id_usuario)
        pedido = Pedido(usuario, forma_pago)

        for id_producto, cantidad in detalles:
            producto = self.__producto_servicio.buscar_por_id(id_producto)
            pedido.agregar_detalle(cantidad, producto)

        for detalle in pedido.detalles:
            producto = detalle.producto
            producto.stock -= detalle.cantidad

        self.__pedidos.append(pedido)
        return pedido

    def _devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad

    def actualizar_forma_pago(self,id_pedido: int,forma_pago: FormaPago,) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        pedido.forma_pago = forma_pago
        return pedido

    def actualizar_estado(self,id_pedido: int,nuevo_estado: Estado,) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)

        pedido.cambiar_estado(nuevo_estado)

        if nuevo_estado == Estado.CANCELADO:
            self._devolver_stock(pedido)

        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)

        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self._devolver_stock(pedido)

        pedido.eliminado = True

        for detalle in pedido.detalles:
            detalle.eliminado = True

    def listar_por_usuario(self, id_usuario: int) -> list[Pedido]:
        return [
            pedido
            for pedido in self.listar()
            if pedido.usuario.id == id_usuario
        ]


    def buscar_para_usuario(self,id_pedido: int,id_usuario: int,) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)

        if pedido.usuario.id != id_usuario:
            raise EntidadNoEncontradaError(
                f"No se encontró el pedido con id {id_pedido}"
            )

        return pedido
