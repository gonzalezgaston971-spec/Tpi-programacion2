from math import isfinite

from entidades.base import Base
from entidades.categoria import Categoria
from excepciones.errores import DatoInvalidoError, TipoDatoInvalidoError


class Producto(Base):
    def __init__(
        self,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
        descripcion: str,
        imagen: str,
        disponible: bool,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagen = imagen
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El nombre debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("El nombre de producto no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TipoDatoInvalidoError("El precio debe ser numérico")
        if not isfinite(valor):
            raise DatoInvalidoError("El precio debe ser un número finito")
        if valor < 0:
            raise DatoInvalidoError("El precio no puede ser negativo")
        self.__precio = float(valor)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TipoDatoInvalidoError("El stock debe ser un número entero")
        if valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo")
        self.__stock = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria):
            raise TipoDatoInvalidoError("La categoría debe ser una instancia de Categoria")
        if valor.eliminado:
            raise DatoInvalidoError("No se puede asignar una categoría eliminada")
        self.__categoria = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("La descripción debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía")
        self.__descripcion = valor.strip()

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("La imagen debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("La imagen no puede estar vacía")
        self.__imagen = valor.strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TipoDatoInvalidoError("Disponible debe ser True o False")
        self.__disponible = valor

    def __str__(self) -> str:
        return (
            f"Producto {self.id}: {self.nombre} - ${self.precio:.2f} "
            f"(stock: {self.stock}, categoría: {self.categoria.nombre})"
        )
