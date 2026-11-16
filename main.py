from consola.entrada import leer_texto
from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from entidades.usuario import Usuario
from enums.tipos import Rol
from excepciones.errores import CredencialesInvalidasError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def crear_menu(
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
) -> Menu:
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(
            usuario,
            categoria_servicio,
            producto_servicio,
            usuario_servicio,
            pedido_servicio,
        )

    return MenuCliente(
        usuario,
        categoria_servicio,
        producto_servicio,
        usuario_servicio,
        pedido_servicio,
    )


def main() -> None:
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio)
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(usuario_servicio, producto_servicio)

    usuario_servicio.crear(
        nombre="Ana",
        apellido="Pérez",
        mail="admin@foodstore.com",
        celular="1100000000",
        contrasenia="admin123",
        rol=Rol.ADMIN,
    )

    while True:
        print("\n=== FOOD STORE - INICIO DE SESIÓN ===")
        usuario_sesion: Usuario | None = None

        for intento in range(1, 4):
            mail = leer_texto("Mail: ")
            contrasenia = leer_texto("Contraseña: ")

            try:
                usuario_sesion = usuario_servicio.autenticar(
                    mail,
                    contrasenia,
                )
                break
            except CredencialesInvalidasError:
                print("Mail o contraseña incorrectos.")

        if usuario_sesion is None:
            print("Se agotaron los tres intentos. El programa termina.")
            return

        print(
            f"Bienvenido/a, {usuario_sesion.nombre} "
            f"{usuario_sesion.apellido} [{usuario_sesion.rol.name}]"
        )

        menu = crear_menu(
            usuario_sesion,
            categoria_servicio,
            producto_servicio,
            usuario_servicio,
            pedido_servicio,
        )

        if not menu.mostrar():
            return


if __name__ == "__main__":
    main()
