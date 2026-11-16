from typing import Callable

from consola.menu import Menu
from consola.entrada import leer_entero, leer_si_no
from excepciones.errores import FoodStoreError


class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - CLIENTE ({self._usuario.nombre}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")

            opcion = leer_entero("Seleccioná una opción: ")

            if opcion == 1:
                self._ejecutar(self._ver_categorias)
            elif opcion == 2:
                self._ejecutar(self._ver_productos)
            elif opcion == 3:
                self._ejecutar(self._ver_pedidos)
            elif opcion == 4:
                self._ejecutar(self._ver_datos)
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

    def _ver_categorias(self) -> None:
        categorias = self._categoria_servicio.listar()

        if not categorias:
            print("No hay categorías cargadas.")
            return

        for categoria in categorias:
            print(categoria)

    def _ver_productos(self) -> None:
        productos = self._producto_servicio.listar_disponibles()

        if not productos:
            print("No hay productos disponibles.")
            return

        for producto in productos:
            print(producto)

    def _ver_pedidos(self) -> None:
        pedidos = self._pedido_servicio.listar_por_usuario(self._usuario.id)

        if not pedidos:
            print("Todavía no tenés pedidos.")
            return

        for pedido in pedidos:
            print(pedido)

        if not leer_si_no("¿Querés consultar los detalles de un pedido?"):
            return

        id_pedido = leer_entero("ID del pedido: ", minimo=1)
        pedido = self._pedido_servicio.buscar_para_usuario(
            id_pedido,
            self._usuario.id,
        )

        for detalle in pedido.detalles:
            print(detalle)

        print(f"Total: ${pedido.total:.2f}")

    def _ver_datos(self) -> None:
        print(f"Nombre: {self._usuario.nombre}")
        print(f"Apellido: {self._usuario.apellido}")
        print(f"Mail: {self._usuario.mail}")
        print(f"Celular: {self._usuario.celular}")
        print(f"Rol: {self._usuario.rol.name}")