from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detallepedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.tipos import Estado, FormaPago
from excepciones.errores import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    TipoDatoInvalidoError,
)


class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        if not isinstance(usuario, Usuario):
            raise TipoDatoInvalidoError("El usuario debe ser una instancia de Usuario")
        if usuario.eliminado:
            raise DatoInvalidoError("No se puede crear un pedido para un usuario eliminado")

        super().__init__()
        self.__usuario: Usuario = usuario
        self.forma_pago = forma_pago
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise TipoDatoInvalidoError("La forma de pago debe ser un valor de FormaPago")
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def __str__(self) -> str:
        return (
            f"Pedido {self.id}: {self.usuario.nombre} {self.usuario.apellido} - "
            f"{self.estado.name} - total ${self.total:.2f}"
        )

    def buscar_detalle_por_producto(
        self,
        producto: Producto,
    ) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(producto, Producto):
            raise TipoDatoInvalidoError("Debe ingresar un producto válido")
        if producto.eliminado:
            raise DatoInvalidoError("No se puede agregar un producto eliminado")

        detalle_existente = self.buscar_detalle_por_producto(producto)
        if detalle_existente is not None:
            detalle_existente._agregar_cantidad(cantidad)
        else:
            self.__detalles.append(
                DetallePedido(cantidad=cantidad, producto=producto)
            )
        self.calcular_total()

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise DatoInvalidoError("El producto no está en este pedido")
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = float(sum(detalle.subtotal for detalle in self.__detalles))

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        if not isinstance(nuevo_estado, Estado):
            raise TipoDatoInvalidoError("El nuevo estado debe ser un valor de Estado")

        transiciones_validas: dict[Estado, tuple[Estado, ...]] = {
            Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
            Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO),
            Estado.TERMINADO: (),
            Estado.CANCELADO: (),
        }
        if nuevo_estado not in transiciones_validas[self.__estado]:
            raise OperacionNoPermitidaError(
                f"No se puede cambiar de {self.__estado.name} "
                f"a {nuevo_estado.name}"
            )
        self.__estado = nuevo_estado
