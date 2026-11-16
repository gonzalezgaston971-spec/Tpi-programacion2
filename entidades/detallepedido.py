from entidades.base import Base
from entidades.producto import Producto
from excepciones.errores import (
    DatoInvalidoError,
    StockInsuficienteError,
    TipoDatoInvalidoError,
)


class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(producto, Producto):
            raise TipoDatoInvalidoError("El producto debe ser una instancia de Producto")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TipoDatoInvalidoError("La cantidad debe ser un número entero")
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser 1 o más")
        if producto.eliminado:
            raise DatoInvalidoError("No se puede agregar un producto eliminado")
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"La cantidad {cantidad} supera el stock disponible "
                f"({producto.stock})"
            )

        super().__init__()
        self.__producto: Producto = producto
        self.__cantidad: int = cantidad
        self.__subtotal: float = float(cantidad * producto.precio)

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return (
            f"{self.cantidad} x {self.producto.nombre} "
            f"(subtotal: ${self.subtotal:.2f})"
        )

    def _agregar_cantidad(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TipoDatoInvalidoError("La cantidad debe ser un número entero")
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero")

        nueva_cantidad = self.__cantidad + cantidad
        if nueva_cantidad > self.__producto.stock:
            raise StockInsuficienteError(
                f"La cantidad total {nueva_cantidad} supera el stock "
                f"disponible ({self.__producto.stock})"
            )

        nuevo_subtotal = self.__subtotal + cantidad * self.__producto.precio
        self.__cantidad = nueva_cantidad
        self.__subtotal = float(nuevo_subtotal)
