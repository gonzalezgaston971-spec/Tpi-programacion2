from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar

from excepciones.errores import TipoDatoInvalidoError


class Base(ABC):
    __siguiente_id: ClassVar[int] = 1

    def __init__(self) -> None:
        self.__id: int = Base.__siguiente_id
        Base.__siguiente_id += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TipoDatoInvalidoError("Eliminado debe ser True o False")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return False
        return self.id == otro.id
