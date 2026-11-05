"""Eliminación de Gauss con pivoteo parcial para sistemas Ax = b."""
from __future__ import annotations

import numpy as np


class SistemaSingularError(ValueError):
    """El sistema no tiene una solución única numéricamente confiable."""


def eliminacion_gauss(A, b, tolerancia: float = 1e-12, cifras_significativas: int | None = None):
    """Resuelve Ax=b y devuelve (x, matriz_aumentada_escalonada).

    Requisitos: A cuadrada y b con la misma cantidad de filas. Usa pivoteo
    parcial para reducir el error numérico y detectar pivotes nulos. Si se
    indica cifras_significativas, redondea cada operación a esa precisión.
    """
    A = np.array(A, dtype=float, copy=True)
    b = np.array(b, dtype=float, copy=True).reshape(-1)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("La matriz de coeficientes A debe ser cuadrada.")
    n = A.shape[0]
    if b.size != n:
        raise ValueError("El vector independiente b debe tener el mismo tamaño que A.")
    if not np.isfinite(A).all() or not np.isfinite(b).all():
        raise ValueError("Todos los valores deben ser números finitos.")
    if cifras_significativas is not None and cifras_significativas < 1:
        raise ValueError("Las cifras significativas deben ser un entero positivo.")

    def redondear(valor):
        if cifras_significativas is None or valor == 0:
            return float(valor)
        return float(f"{valor:.{cifras_significativas}g}")

    aumentada = np.column_stack((A, b))
    escala = max(1.0, float(np.linalg.norm(A, ord=np.inf)))
    umbral = tolerancia * escala

    # Eliminación hacia adelante con pivoteo parcial.
    for columna in range(n):
        fila_pivote = columna + int(np.argmax(np.abs(aumentada[columna:, columna])))
        if abs(aumentada[fila_pivote, columna]) <= umbral:
            raise SistemaSingularError(
                "No hay pivote distinto de cero: el sistema es singular o casi singular "
                "y no tiene una solución única confiable."
            )
        if fila_pivote != columna:
            aumentada[[columna, fila_pivote]] = aumentada[[fila_pivote, columna]]

        for fila in range(columna + 1, n):
            factor = redondear(aumentada[fila, columna] / aumentada[columna, columna])
            for j in range(columna + 1, n + 1):
                producto = redondear(factor * aumentada[columna, j])
                aumentada[fila, j] = redondear(aumentada[fila, j] - producto)
            aumentada[fila, columna] = 0.0

    # Sustitución regresiva.
    x = np.zeros(n, dtype=float)
    for fila in range(n - 1, -1, -1):
        resto = 0.0
        for j in range(fila + 1, n):
            resto = redondear(resto + redondear(aumentada[fila, j] * x[j]))
        x[fila] = redondear((aumentada[fila, n] - resto) / aumentada[fila, fila])

    return x, aumentada
