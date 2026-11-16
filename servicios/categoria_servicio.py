from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.errores import (
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    TipoDatoInvalidoError,
)


class CategoriaServicio:
    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        return [categoria for categoria in self.__categorias if not categoria.eliminado]

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(
            f"No se encontró la categoría con id {id_categoria}"
        )

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if not isinstance(nombre, str) or not isinstance(descripcion, str):
            raise TipoDatoInvalidoError("Nombre y descripción deben ser texto")
        nombre_limpio = nombre.strip()
        descripcion_limpia = descripcion.strip()
        if not nombre_limpio or not descripcion_limpia:
            raise DatoInvalidoError("Nombre y descripción son obligatorios")
        if any(
            categoria.nombre.strip().casefold() == nombre_limpio.casefold()
            for categoria in self.__categorias
        ):
            raise DuplicadoError(f"Ya existe una categoría llamada '{nombre_limpio}'")

        nueva_categoria = Categoria(nombre_limpio, descripcion_limpia)
        self.__categorias.append(nueva_categoria)
        return nueva_categoria

    def editar(
        self,
        id_categoria: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None and not isinstance(nombre, str):
            raise TipoDatoInvalidoError("El nombre debe ser texto")
        if descripcion is not None and not isinstance(descripcion, str):
            raise TipoDatoInvalidoError("La descripción debe ser texto")

        nombre_nuevo = nombre.strip() if nombre and nombre.strip() else categoria.nombre
        descripcion_nueva = (
            descripcion.strip()
            if descripcion and descripcion.strip()
            else categoria.descripcion
        )
        if any(
            otra.id != categoria.id
            and otra.nombre.strip().casefold() == nombre_nuevo.casefold()
            for otra in self.__categorias
        ):
            raise DuplicadoError(f"Ya existe una categoría llamada '{nombre_nuevo}'")
        if not nombre_nuevo or not descripcion_nueva:
            raise DatoInvalidoError("Nombre y descripción son obligatorios")

        categoria.nombre = nombre_nuevo
        categoria.descripcion = descripcion_nueva
        return categoria

    def eliminar(
        self,
        id_categoria: int,
        productos_activos: list[Producto],
    ) -> None:
        categoria = self.buscar_por_id(id_categoria)
        productos_asociados = [
            producto
            for producto in productos_activos
            if producto.categoria == categoria
        ]
        if productos_asociados:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría: tiene "
                f"{len(productos_asociados)} producto(s) activo(s)"
            )
        categoria.eliminado = True
