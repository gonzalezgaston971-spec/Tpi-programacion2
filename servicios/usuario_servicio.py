from entidades.usuario import Usuario
from enums.tipos import Rol
from excepciones.errores import (
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    TipoDatoInvalidoError,
)


class UsuarioServicio:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def listar(self) -> list[Usuario]:
        return [usuario for usuario in self.__usuarios if not usuario.eliminado]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(
            f"No se encontró el usuario con id {id_usuario}"
        )

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        if not isinstance(mail, str):
            raise TipoDatoInvalidoError("El mail debe ser texto")
        mail_limpio = mail.strip()
        mail_normalizado = mail_limpio.casefold()
        if any(usuario.mail.casefold() == mail_normalizado for usuario in self.__usuarios):
            raise DuplicadoError(f"Ya existe un usuario con el mail '{mail_limpio}'")

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            mail=mail_limpio,
            celular=celular,
            contrasenia=contrasenia,
            rol=rol,
        )
        self.__usuarios.append(nuevo_usuario)
        return nuevo_usuario

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        if not isinstance(mail, str) or not isinstance(contrasenia, str):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        mail_normalizado = mail.strip().casefold()
        for usuario in self.__usuarios:
            if (
                usuario.mail.casefold() == mail_normalizado
                and not usuario.eliminado
                and usuario.verificar_contrasenia(contrasenia)
            ):
                return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)
        campos_texto = (nombre, apellido, mail, celular)
        if any(valor is not None and not isinstance(valor, str) for valor in campos_texto):
            raise TipoDatoInvalidoError("Los datos del usuario deben ser texto")
        if rol is not None and not isinstance(rol, Rol):
            raise TipoDatoInvalidoError("El rol debe ser ADMIN o USUARIO")

        nombre_nuevo = nombre.strip() if nombre and nombre.strip() else usuario.nombre
        apellido_nuevo = (
            apellido.strip() if apellido and apellido.strip() else usuario.apellido
        )
        mail_nuevo = mail.strip() if mail and mail.strip() else usuario.mail
        celular_nuevo = (
            celular.strip() if celular and celular.strip() else usuario.celular
        )

        if "@" not in mail_nuevo or "." not in mail_nuevo:
            raise DatoInvalidoError("El mail debe tener un formato válido con @ y .")
        if any(
            otro.id != usuario.id
            and otro.mail.casefold() == mail_nuevo.casefold()
            for otro in self.__usuarios
        ):
            raise DuplicadoError(f"Ya existe un usuario con el mail '{mail_nuevo}'")

        usuario.nombre = nombre_nuevo
        usuario.apellido = apellido_nuevo
        usuario.mail = mail_nuevo
        usuario.celular = celular_nuevo
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        usuario = self.buscar_por_id(id_usuario)
        if usuario.id == usuario_sesion.id:
            raise OperacionNoPermitidaError(
                "No podés eliminar al usuario que tiene la sesión iniciada"
            )
        usuario.eliminado = True
