from entidades.base import Base
from enums.tipos import Rol
from excepciones.errores import DatoInvalidoError, TipoDatoInvalidoError


class Usuario(Base):
    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        if not isinstance(contrasenia, str):
            raise TipoDatoInvalidoError("La contraseña debe ser texto")
        if not contrasenia:
            raise DatoInvalidoError("La contraseña no puede estar vacía")
        self.__contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El nombre debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El apellido debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El mail debe ser texto")
        mail_limpio = valor.strip()
        if not mail_limpio or "@" not in mail_limpio or "." not in mail_limpio:
            raise DatoInvalidoError("El mail debe tener un formato válido con @ y .")
        self.__mail = mail_limpio

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TipoDatoInvalidoError("El celular debe ser texto")
        if not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío")
        self.__celular = valor.strip()

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise TipoDatoInvalidoError("El rol debe ser ADMIN o USUARIO")
        self.__rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"Usuario {self.id}: {self.nombre} {self.apellido} ({self.rol.name})"
