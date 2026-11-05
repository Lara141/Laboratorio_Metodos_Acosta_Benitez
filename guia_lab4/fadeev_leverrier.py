"""Método de Faddeev-Leverrier para el polinomio característico y autovectores."""
from __future__ import annotations

import numpy as np


def fadeev_leverrier(A, tolerancia: float = 1e-10):
    """Calcula coeficientes de det(lambda I-A) y autovalores/autovectores.

    Retorna un diccionario con coefficients [1,c1,...,cn], eigenvalues,
    eigenvectors (columnas), residuals y la matriz inversa cuando existe.
    Requisito: A cuadrada. Los autovalores se obtienen como raíces del
    polinomio característico generado por la recurrencia de Faddeev-Leverrier.
    """
    A = np.array(A, dtype=float, copy=True)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada para hallar autovalores.")
    if not np.isfinite(A).all():
        raise ValueError("Todos los valores de A deben ser números finitos.")

    n = A.shape[0]
    identidad = np.eye(n)
    B = identidad.copy()
    coeficientes = [1.0]

    # p(lambda)=lambda^n+c1 lambda^(n-1)+...+cn
    for k in range(1, n + 1):
        c_k = -np.trace(A @ B) / k
        coeficientes.append(float(c_k))
        B = A @ B + c_k * identidad

    coeficientes_array = np.array(coeficientes, dtype=float)
    autovalores = np.roots(coeficientes_array)
    # NumPy ya devuelve el multiconjunto de raíces. Para cada raíz obtenemos
    # un vector unitario asociado mediante el último vector singular derecho.
    autovectores = np.zeros((n, n), dtype=complex)
    residuos = np.zeros(n, dtype=float)
    for j, valor in enumerate(autovalores):
        M = A.astype(complex) - valor * identidad
        _, _, vh = np.linalg.svd(M)
        vector = vh.conj().T[:, -1]
        norma = np.linalg.norm(vector)
        if norma == 0:
            raise ArithmeticError("No fue posible obtener un autovector numérico.")
        vector = vector / norma
        # Fija la fase para mostrar resultados reproducibles (primer elemento
        # de módulo apreciable real y no negativo cuando sea posible).
        primero = next((v for v in vector if abs(v) > tolerancia), None)
        if primero is not None:
            vector *= np.exp(-1j * np.angle(primero))
        if np.max(np.abs(vector.imag)) < tolerancia:
            vector = vector.real.astype(complex)
        autovectores[:, j] = vector
        residuos[j] = float(np.linalg.norm(A @ vector - valor * vector))

    determinante = float(np.linalg.det(A))
    inversa = None
    if abs(determinante) > tolerancia:
        # B_n = 0 en aritmética exacta; al terminar el ciclo B guarda B_n.
        # A^{-1}=-B_(n-1)/c_n; se reconstruye B_(n-1) para evitar confundirlo
        # con B_n.
        B_anterior = identidad.copy()
        for k in range(1, n):
            c_k = coeficientes[k]
            B_anterior = A @ B_anterior + c_k * identidad
        inversa = -B_anterior / coeficientes[-1]

    return {
        "coefficients": coeficientes_array,
        "eigenvalues": autovalores,
        "eigenvectors": autovectores,
        "residuals": residuos,
        "inverse": inversa,
        "determinant": determinante,
    }
