from __future__ import annotations

import numpy as np


def leer_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("Ingresá un entero mayor que cero.")
        except ValueError:
            print("Entrada inválida: ingresá un número entero.")


def leer_matriz(n: int, nombre: str = "A") -> np.ndarray:
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
    for i, valor in enumerate(vector, start=1):
        print(f"{variable}{i} = {np.real_if_close(valor)}")
