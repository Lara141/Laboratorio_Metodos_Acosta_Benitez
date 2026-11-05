from __future__ import annotations

import time
import numpy as np

from entrada import leer_entero_positivo, leer_matriz, leer_vector, imprimir_vector
from gauss import eliminacion_gauss, SistemaSingularError
from fadeev_leverrier import fadeev_leverrier

def ejecutar_gauss():
    print("\n=== Eliminación de Gauss ===")
    n = leer_entero_positivo("Cantidad de ecuaciones/incógnitas: ")
    A = leer_matriz(n, "A")
    b = leer_vector(n, "b")
    precision = input("Cifras significativas (Enter = precisión completa; para el ejercicio 1 use 3): ").strip()
    
    try:
        cifras = int(precision) if precision else None
        inicio = time.perf_counter()
        
        x, triangular = eliminacion_gauss(A, b, cifras_significativas=cifras)
    except (ValueError, SistemaSingularError) as error:
        print(f"\nNo se pudo resolver: {error}")
        return
        
    fin = time.perf_counter()
    print(f"\nResiduo ||Ax-b||₂ = {np.linalg.norm(A @ x - b):.6g}")
    print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")

    # Menú iterativo para el cálculo del costo
    while True:
        respuesta = input("\n¿Desea calcular el costo total? (s/n): ").strip().lower()
        if respuesta in ['s', 'si', 'sí']:
            costo_texto = input("Ingrese los coeficientes de costo por incógnita (separados por espacios): ").strip()
            try:
                costos = np.array([float(v.replace(",", ".")) for v in costo_texto.split()])
                if costos.size != n:
                    print(f"Se esperaban {n} coeficientes de costo; no se calculó el total.")
                else:
                    print(f"Costo total = {np.dot(costos, x):.10g}")
            except ValueError:
                print("No se pudo calcular el costo: ingresá números separados por espacios.")
            break
        elif respuesta in ['n', 'no']:
            break
        else:
            print("Por favor, responda 's' (sí) o 'n' (no).")


def ejecutar_fadeev():
    print("\n=== Faddeev-Leverrier ===")
    n = leer_entero_positivo("Orden de la matriz cuadrada A: ")
    A = leer_matriz(n, "A")
    try:
        resultado = fadeev_leverrier(A)
    except (ValueError, ArithmeticError, np.linalg.LinAlgError) as error:
        print(f"No se pudo completar el cálculo: {error}")
        return
    print("\nPolinomio característico p(λ) = det(λI - A):")
    coef = resultado["coefficients"]
    terminos = [f"λ^{n}"]
    for k, c in enumerate(coef[1:], start=1):
        potencia = n - k
        terminos.append(f"({c:.10g})" + (f" λ^{potencia}" if potencia > 1 else " λ" if potencia == 1 else ""))
    print(" + ".join(terminos))
    print("\nAutovalores y autovectores (cada columna corresponde al autovalor de igual índice):")
    for j, valor in enumerate(resultado["eigenvalues"]):
        vector = np.real_if_close(resultado["eigenvectors"][:, j], tol=1000)
        valor = np.real_if_close(valor, tol=1000)
        print(f"\nλ{j + 1} = {valor}")
        imprimir_vector(vector, f"v{j + 1}_")
        print(f"Residuo ||Av-λv||₂ = {resultado['residuals'][j]:.6g}")
    print(f"\nDeterminante de A = {resultado['determinant']:.10g}")
    if resultado["inverse"] is not None:
        print("A es no singular; inversa obtenida por Faddeev-Leverrier:")
        print(np.array2string(resultado["inverse"], precision=8, suppress_small=True))
    else:
        print("A es singular (o numéricamente cercana a singular); no existe A⁻¹.")


def main():
    while True:
        print("\nLABORATORIO 4 — SISTEMAS DE ECUACIONES")
        print("1. Resolver Ax=b por Eliminación de Gauss")
        print("2. Analizar A por Faddeev-Leverrier")
        print("0. Salir")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            ejecutar_gauss()
        elif opcion == "2":
            ejecutar_fadeev()
        elif opcion == "0":
            print("Fin del programa.")
            break
        else:
            print("Opción inválida. Elegí 0, 1 o 2.")


if __name__ == "__main__":
    main()
