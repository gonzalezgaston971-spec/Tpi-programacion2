from entidades.base import Base
from excepciones.errores import DatoInvalidoError, TipoDatoInvalidoError


class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El nombre debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("El nombre de categoría no puede estar vacío")
        self.__nombre = valor.strip()

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

    def __str__(self) -> str:
        return f"Categoría {self.id}: {self.nombre} - {self.descripcion}"
