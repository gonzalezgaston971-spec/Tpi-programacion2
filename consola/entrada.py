import os
import sys
from enum import Enum
from math import isfinite
from typing import TypeVar

E = TypeVar("E", bound=Enum)


def _leer(mensaje: str) -> str:
    respuesta = input(mensaje)
    if sys.stdin.isatty() and sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")
    return respuesta


def leer_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        texto = _leer(mensaje).strip()
        if texto or permitir_vacio:
            return texto
        print("El texto no puede estar vacío.")


def leer_entero(
    mensaje: str,
    minimo: int | None = None,
    maximo: int | None = None,
) -> int:
    while True:
        try:
            valor = int(_leer(mensaje))
        except ValueError:
            print("Ingresá un número entero válido.")
            continue

        if minimo is not None and valor < minimo:
            print(f"El valor mínimo permitido es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"El valor máximo permitido es {maximo}.")
            continue
        return valor


def leer_float(
    mensaje: str,
    minimo: float | None = None,
    maximo: float | None = None,
) -> float:
    while True:
        texto = _leer(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("Ingresá un número válido.")
            continue

        if not isfinite(valor):
            print("Ingresá un número finito.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor mínimo permitido es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"El valor máximo permitido es {maximo}.")
            continue
        return valor


def leer_si_no(mensaje: str) -> bool:
    while True:
        respuesta = _leer(f"{mensaje} (S/N): ").strip().casefold()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respondé S o N.")


def leer_enum(mensaje: str, tipo_enum: type[E]) -> E:
    opciones = list(tipo_enum)
    if not opciones:
        raise ValueError("El enumerado no tiene opciones.")

    print(mensaje)
    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion.name}")

    seleccion = leer_entero(
        "Seleccioná una opción: ",
        minimo=1,
        maximo=len(opciones),
    )
    return opciones[seleccion - 1]
