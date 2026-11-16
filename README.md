# Food Store

Trabajo Práctico Integrador de Programación II. Aplicación de consola para gestionar categorías, productos, usuarios y pedidos de un negocio de comidas.

## Requisitos

- Python 3.12 o superior
- No requiere instalar bibliotecas externas

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

El programa inicia con un administrador:

- Mail: `admin@foodstore.com`
- Contraseña: `admin123`

Los datos se mantienen en memoria mientras el programa está abierto. Al salir, se pierden.

## Pruebas

Desde la carpeta raíz:

```bash
python -m unittest -v pruebas
```

Las pruebas cubren autenticación, categorías duplicadas, reglas de stock, pedidos, cancelación, bajas lógicas y acceso a pedidos propios.

## Organización

```text
food_store/
├── main.py
├── pruebas.py
├── consola/
├── entidades/
├── enums/
├── excepciones/
└── servicios/
```

- `entidades/`: modelo orientado a objetos y validaciones de atributos.
- `enums/`: roles, estados y formas de pago.
- `excepciones/`: errores del dominio.
- `servicios/`: colecciones en memoria y reglas de negocio.
- `consola/`: lectura validada y menús por rol.
- `main.py`: inicialización de servicios, sesión y selección de menú.
- `pruebas.py`: pruebas automatizadas con `unittest`.

## Funcionalidades

El administrador puede gestionar categorías, productos y usuarios, y crear, consultar, actualizar y dar de baja pedidos. El cliente puede consultar categorías, productos disponibles, sus datos y sus propios pedidos.

Las bajas son lógicas. La creación de pedidos valida todos los detalles antes de descontar stock. Al cancelar un pedido pendiente o confirmado, el stock vuelve a los productos. Las lecturas de consola limpian la pantalla después de cada entrada en una terminal interactiva.

## Entregables y enlaces

- Informe: `Informe_TPI_FoodStore.pdf`
- Repositorio: `https://github.com/gonzalezgaston971-spec/Tpi_programacion2.git`
- Video público: pendiente de grabación y publicación.

## Créditos

- Estudiante: Gaston Gonzalez
- Fecha de entrega: 15/11/2026
