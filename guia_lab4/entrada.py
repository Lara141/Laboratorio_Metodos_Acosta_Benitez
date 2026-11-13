"""Funciones auxiliares para leer datos desde la consola.

Este módulo centraliza la validación de entradas del usuario para reutilizarse
desde el programa principal y las distintas rutinas numéricas.
"""

from __future__ import annotations

import numpy as np


def leer_entero_positivo(mensaje: str) -> int:
    """Solicita un entero positivo al usuario.

    Args:
        mensaje: Texto a mostrar antes de pedir el valor.

    Returns:
        Un entero mayor que cero.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("Ingresá un entero mayor que cero.")
        except ValueError:
            print("Entrada inválida: ingresá un número entero.")

 
def leer_matriz(n: int, nombre: str = "A") -> np.ndarray:
    """Lee una matriz de tamaño n x n desde la entrada estándar.

    Args:
        n: Orden de la matriz.
        nombre: Etiqueta usada para identificar la matriz.

    Returns:
        Una matriz NumPy con los números ingresados por el usuario.
    """
    print(f"Ingresá {n} filas para la matriz {nombre}, con {n} números separados por espacios.")
    filas = []
    for i in range(n):
        while True:
            try:
                valores = [float(v.replace(",", ".")) for v in input(f"Fila {i + 1}: ").split()]
                if len(valores) != n:
                    print(f"Se esperaban {n} valores; recibí {len(valores)}.")
                    continue
                filas.append(valores)
                break
            except ValueError:
                print("Fila inválida. Usá números separados por espacios.")
    return np.array(filas, dtype=float)


def leer_vector(n: int, nombre: str = "b") -> np.ndarray:
    """Lee un vector de dimensión n desde la entrada estándar.

    Args:
        n: Cantidad de componentes del vector.
        nombre: Nombre que se muestra al pedir los datos.

    Returns:
        Vector NumPy con los valores ingresados.
    """
    while True:
        try:
            valores = [float(v.replace(",", ".")) for v in input(f"Ingresá {n} valores para {nombre}: ").split()]
            if len(valores) != n:
                print(f"Se esperaban {n} valores; recibí {len(valores)}.")
                continue
            return np.array(valores, dtype=float)
        except ValueError:
            print("Entrada inválida. Usá números separados por espacios.")


def imprimir_vector(vector, variable: str = "x") -> None:
    """Muestra un vector con formato variable_i = valor.

    Args:
        vector: Secuencia de valores a mostrar.
        variable: Prefijo utilizado en cada componente del vector.
    """
    for i, valor in enumerate(vector, start=1):
        print(f"{variable}{i} = {np.real_if_close(valor)}")
