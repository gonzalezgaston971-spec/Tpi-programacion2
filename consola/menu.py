from abc import ABC, abstractmethod

from entidades.usuario import Usuario
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio


class Menu(ABC):
    def __init__(self,usuario: Usuario,categoria_servicio: CategoriaServicio,producto_servicio: ProductoServicio,usuario_servicio: UsuarioServicio,pedido_servicio: PedidoServicio,) -> None:
        self._usuario: Usuario = usuario
        self._categoria_servicio: CategoriaServicio = categoria_servicio
        self._producto_servicio: ProductoServicio = producto_servicio
        self._usuario_servicio: UsuarioServicio = usuario_servicio
        self._pedido_servicio: PedidoServicio = pedido_servicio

    @abstractmethod
    def mostrar(self) -> bool:
        pass
