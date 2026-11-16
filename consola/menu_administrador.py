from math import isfinite
from typing import Callable, TypeVar
from enum import Enum

from consola.menu import Menu
from consola.entrada import (
    leer_entero,
    leer_enum,
    leer_float,
    leer_si_no,
    leer_texto,
)
from enums.tipos import Estado, FormaPago, Rol
from excepciones.errores import FoodStoreError


E = TypeVar("E", bound=Enum)


class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - ADMINISTRADOR ({self._usuario.nombre}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")

            opcion = leer_entero("Seleccioná una opción: ")

            if opcion == 1:
                self._menu_categorias()
            elif opcion == 2:
                self._menu_productos()
            elif opcion == 3:
                self._menu_usuarios()
            elif opcion == 4:
                self._menu_pedidos()
            elif opcion == 9:
                return True
            elif opcion == 0:
                return False
            else:
                print("Opción fuera de rango.")

    def _ejecutar(self, accion: Callable[[], None]) -> None:
        try:
            accion()
        except (FoodStoreError, ValueError, TypeError) as error:
            print(f"Error: {error}")

    def _submenu(
        self,
        titulo: str,
        opciones: dict[int, tuple[str, Callable[[], None]]],
    ) -> None:
        while True:
            print(f"\n--- {titulo} ---")
            for numero, (nombre, _) in opciones.items():
                print(f"{numero}. {nombre}")
            print("0. Volver")

            opcion = leer_entero("Seleccioná una opción: ")

            if opcion == 0:
                return

            if opcion not in opciones:
                print("Opción fuera de rango.")
                continue

            self._ejecutar(opciones[opcion][1])

    def _leer_float_opcional(self, mensaje: str) -> float | None:
        texto = leer_texto(mensaje, permitir_vacio=True)
        if not texto:
            return None

        valor = float(texto.replace(",", "."))
        if not isfinite(valor):
            raise ValueError("Ingresá un número finito.")
        return valor

    def _leer_entero_opcional(self, mensaje: str) -> int | None:
        texto = leer_texto(mensaje, permitir_vacio=True)
        if not texto:
            return None
        return int(texto)

    def _leer_booleano_opcional(self, mensaje: str) -> bool | None:
        texto = leer_texto(mensaje, permitir_vacio=True).casefold()

        if not texto:
            return None
        if texto in ("s", "si", "sí"):
            return True
        if texto in ("n", "no"):
            return False

        raise ValueError("Ingresá S, N o dejá el campo vacío.")

    def _leer_enum_opcional(self, mensaje: str, tipo_enum: type[E]) -> E | None:
        opciones = list(tipo_enum)

        print(mensaje)
        for indice, opcion in enumerate(opciones, start=1):
            print(f"{indice}. {opcion.name}")

        texto = leer_texto(
            "Número de opción (Enter para conservar): ",
            permitir_vacio=True,
        )

        if not texto:
            return None

        indice = int(texto)
        if indice < 1 or indice > len(opciones):
            raise ValueError("La opción elegida no existe.")

        return opciones[indice - 1]

    def _menu_categorias(self) -> None:
        self._submenu(
            "CATEGORÍAS",
            {
                1: ("Listar", self._listar_categorias),
                2: ("Crear", self._crear_categoria),
                3: ("Editar", self._editar_categoria),
                4: ("Eliminar", self._eliminar_categoria),
            },
        )

    def _listar_categorias(self) -> None:
        categorias = self._categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas.")
            return

        for categoria in categorias:
            print(categoria)

    def _crear_categoria(self) -> None:
        nombre = leer_texto("Nombre: ")
        descripcion = leer_texto("Descripción: ")

        categoria = self._categoria_servicio.crear(nombre, descripcion)
        print(f"Categoría creada con id {categoria.id}.")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        id_categoria = leer_entero("ID de la categoría: ", minimo=1)
        nombre = leer_texto(
            "Nuevo nombre (Enter conserva el actual): ",
            permitir_vacio=True,
        )
        descripcion = leer_texto(
            "Nueva descripción (Enter conserva la actual): ",
            permitir_vacio=True,
        )

        categoria = self._categoria_servicio.editar(
            id_categoria,
            nombre or None,
            descripcion or None,
        )
        print(f"Categoría actualizada: {categoria}")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        id_categoria = leer_entero("ID de la categoría: ", minimo=1)

        if not leer_si_no("¿Confirmás la baja lógica?"):
            print("Operación cancelada.")
            return

        self._categoria_servicio.eliminar(
            id_categoria,
            self._producto_servicio.listar(),
        )
        print("Categoría eliminada.")

    def _menu_productos(self) -> None:
        self._submenu(
            "PRODUCTOS",
            {
                1: ("Listar", self._listar_productos),
                2: ("Crear", self._crear_producto),
                3: ("Editar", self._editar_producto),
                4: ("Eliminar", self._eliminar_producto),
            },
        )

    def _listar_productos(self) -> None:
        productos = self._producto_servicio.listar()
        if not productos:
            print("No hay productos cargados.")
            return

        for producto in productos:
            print(producto)

    def _crear_producto(self) -> None:
        self._listar_categorias()
        id_categoria = leer_entero("ID de la categoría: ", minimo=1)

        producto = self._producto_servicio.crear(
            nombre=leer_texto("Nombre: "),
            precio=leer_float("Precio: $", minimo=0),
            stock=leer_entero("Stock: ", minimo=0),
            id_categoria=id_categoria,
            descripcion=leer_texto("Descripción: "),
            imagen=leer_texto("Imagen: "),
            disponible=leer_si_no("¿Está disponible?"),
        )
        print(f"Producto creado con id {producto.id}.")

    def _editar_producto(self) -> None:
        self._listar_productos()
        id_producto = leer_entero("ID del producto: ", minimo=1)

        self._listar_categorias()
        print("Dejá un campo vacío para conservar su valor.")

        producto = self._producto_servicio.editar(
            id_producto=id_producto,
            nombre=leer_texto("Nuevo nombre: ", permitir_vacio=True) or None,
            precio=self._leer_float_opcional("Nuevo precio: $"),
            stock=self._leer_entero_opcional("Nuevo stock: "),
            id_categoria=self._leer_entero_opcional("Nuevo ID de categoría: "),
            descripcion=leer_texto(
                "Nueva descripción: ",
                permitir_vacio=True,
            ) or None,
            imagen=leer_texto("Nueva imagen: ", permitir_vacio=True) or None,
            disponible=self._leer_booleano_opcional(
                "¿Disponible? (S/N, Enter conserva): "
            ),
        )
        print(f"Producto actualizado: {producto}")

    def _eliminar_producto(self) -> None:
        self._listar_productos()
        id_producto = leer_entero("ID del producto: ", minimo=1)

        if not leer_si_no("¿Confirmás la baja lógica?"):
            print("Operación cancelada.")
            return

        self._producto_servicio.eliminar(id_producto)
        print("Producto eliminado.")

    def _menu_usuarios(self) -> None:
        self._submenu(
            "USUARIOS",
            {
                1: ("Listar", self._listar_usuarios),
                2: ("Crear", self._crear_usuario),
                3: ("Editar", self._editar_usuario),
                4: ("Eliminar", self._eliminar_usuario),
            },
        )

    def _listar_usuarios(self) -> None:
        usuarios = self._usuario_servicio.listar()
        if not usuarios:
            print("No hay usuarios cargados.")
            return

        for usuario in usuarios:
            print(usuario)

    def _crear_usuario(self) -> None:
        rol = leer_enum("Rol del usuario:", Rol)

        usuario = self._usuario_servicio.crear(
            nombre=leer_texto("Nombre: "),
            apellido=leer_texto("Apellido: "),
            mail=leer_texto("Mail: "),
            celular=leer_texto("Celular: "),
            contrasenia=leer_texto("Contraseña: "),
            rol=rol,
        )
        print(f"Usuario creado con id {usuario.id}.")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        id_usuario = leer_entero("ID del usuario: ", minimo=1)

        print("Dejá un campo vacío para conservar su valor.")
        rol = self._leer_enum_opcional("Nuevo rol:", Rol)

        usuario = self._usuario_servicio.editar(
            id_usuario=id_usuario,
            nombre=leer_texto("Nuevo nombre: ", permitir_vacio=True) or None,
            apellido=leer_texto("Nuevo apellido: ", permitir_vacio=True) or None,
            mail=leer_texto("Nuevo mail: ", permitir_vacio=True) or None,
            celular=leer_texto("Nuevo celular: ", permitir_vacio=True) or None,
            rol=rol,
        )
        print(f"Usuario actualizado: {usuario}")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        id_usuario = leer_entero("ID del usuario: ", minimo=1)

        if not leer_si_no("¿Confirmás la baja lógica?"):
            print("Operación cancelada.")
            return

        self._usuario_servicio.eliminar(id_usuario, self._usuario)
        print("Usuario eliminado.")

    def _menu_pedidos(self) -> None:
        self._submenu(
            "PEDIDOS",
            {
                1: ("Listar", self._listar_pedidos),
                2: ("Crear", self._crear_pedido),
                3: ("Cambiar estado", self._cambiar_estado_pedido),
                4: ("Cambiar forma de pago", self._cambiar_pago_pedido),
                5: ("Eliminar", self._eliminar_pedido),
            },
        )

    def _listar_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar()
        if not pedidos:
            print("No hay pedidos cargados.")
            return

        for pedido in pedidos:
            print(pedido)

    def _crear_pedido(self) -> None:
        self._listar_usuarios()
        id_usuario = leer_entero("ID del usuario: ", minimo=1)
        forma_pago = leer_enum("Forma de pago:", FormaPago)

        self._listar_productos()
        detalles: list[tuple[int, int]] = []

        while True:
            id_producto = leer_entero("ID del producto: ", minimo=1)
            cantidad = leer_entero("Cantidad: ", minimo=1)
            detalles.append((id_producto, cantidad))

            if not leer_si_no("¿Agregar otro producto?"):
                break

        pedido = self._pedido_servicio.crear(
            id_usuario=id_usuario,
            forma_pago=forma_pago,
            detalles=detalles,
        )
        print(f"Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")

    def _cambiar_estado_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido = leer_entero("ID del pedido: ", minimo=1)
        nuevo_estado = leer_enum("Nuevo estado:", Estado)

        pedido = self._pedido_servicio.actualizar_estado(
            id_pedido,
            nuevo_estado,
        )
        print(f"Estado actualizado: {pedido.estado.name}")

    def _cambiar_pago_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido = leer_entero("ID del pedido: ", minimo=1)
        forma_pago = leer_enum("Nueva forma de pago:", FormaPago)

        pedido = self._pedido_servicio.actualizar_forma_pago(
            id_pedido,
            forma_pago,
        )
        print(f"Forma de pago actualizada: {pedido.forma_pago.name}")

    def _eliminar_pedido(self) -> None:
        self._listar_pedidos()
        id_pedido = leer_entero("ID del pedido: ", minimo=1)

        if not leer_si_no("¿Confirmás la baja lógica?"):
            print("Operación cancelada.")
            return

        self._pedido_servicio.eliminar(id_pedido)
        print("Pedido eliminado.")
