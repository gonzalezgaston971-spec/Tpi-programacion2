from entidades.producto import Producto
from servicios.categoria_servicio import CategoriaServicio
from excepciones.errores import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    TipoDatoInvalidoError,
)


class ProductoServicio:
    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__productos: list[Producto] = []
        self.__categoria_servicio: CategoriaServicio = categoria_servicio

    def listar(self) -> list[Producto]:
        return [
            producto
            for producto in self.__productos
            if not producto.eliminado
        ]

    def listar_disponibles(self) -> list[Producto]:
        return [
            producto
            for producto in self.__productos
            if (
                not producto.eliminado
                and producto.disponible
                and producto.stock > 0
            )
        ]

    def buscar_por_id(self, id_producto: int) -> Producto:
        for producto in self.__productos:
            if producto.id == id_producto and not producto.eliminado:
                return producto

        raise EntidadNoEncontradaError(
            f"No se encontró el producto con id {id_producto}"
        )

    def crear(
        self,
        nombre: str,
        precio: float,
        stock: int,
        id_categoria: int,
        descripcion: str,
        imagen: str,
        disponible: bool,
    ) -> Producto:
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)

        nuevo_producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria=categoria,
            descripcion=descripcion,
            imagen=imagen,
            disponible=disponible,
        )

        self.__productos.append(nuevo_producto)
        return nuevo_producto

    def editar(
        self,
        id_producto: int,
        nombre: str | None = None,
        precio: float | None = None,
        stock: int | None = None,
        id_categoria: int | None = None,
        descripcion: str | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
    ) -> Producto:
        producto = self.buscar_por_id(id_producto)

        nombre_nuevo = (
            nombre.strip()
            if nombre is not None and nombre.strip()
            else producto.nombre
        )
        descripcion_nueva = (
            descripcion.strip()
            if descripcion is not None and descripcion.strip()
            else producto.descripcion
        )
        imagen_nueva = (
            imagen.strip()
            if imagen is not None and imagen.strip()
            else producto.imagen
        )

        precio_nuevo = producto.precio if precio is None else precio
        stock_nuevo = producto.stock if stock is None else stock
        disponible_nuevo = (
            producto.disponible if disponible is None else disponible
        )

        if not isinstance(precio_nuevo, (int, float)) or isinstance(precio_nuevo, bool):
            raise TipoDatoInvalidoError("El precio debe ser numérico")
        if precio_nuevo < 0:
            raise DatoInvalidoError("El precio no puede ser negativo")

        if not isinstance(stock_nuevo, int) or isinstance(stock_nuevo, bool):
            raise TipoDatoInvalidoError("El stock debe ser un número entero")
        if stock_nuevo < 0:
            raise DatoInvalidoError("El stock no puede ser negativo")

        if not isinstance(disponible_nuevo, bool):
            raise TipoDatoInvalidoError(
                "Disponible debe ser True o False"
            )

        categoria_nueva = (
            producto.categoria
            if id_categoria is None
            else self.__categoria_servicio.buscar_por_id(id_categoria)
        )

        producto.nombre = nombre_nuevo
        producto.precio = float(precio_nuevo)
        producto.stock = stock_nuevo
        producto.categoria = categoria_nueva
        producto.descripcion = descripcion_nueva
        producto.imagen = imagen_nueva
        producto.disponible = disponible_nuevo

        return producto

    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True
