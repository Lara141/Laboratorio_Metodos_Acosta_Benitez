from __future__ import annotations

import numpy as np


class SistemaSingularError(ValueError):
    """El sistema no tiene una solución única numéricamente confiable."""


def eliminacion_gauss(A, b, tolerancia: float = 1e-12, cifras_significativas: int | None = None):
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
            resultado = float(valor)
        else:
            resultado = float(f"{valor:.{cifras_significativas}g}")
        return 0.0 if resultado == 0 else resultado

    def formatear_numero(valor):
        """Muestra números sin el punto decimal sobrante ni el cero negativo."""
        valor = float(valor)
        if valor == 0:
            return "0"
        return f"{valor:.15g}"

    def matriz_a_texto(matriz, precision=6):
        """Formatea matrices y normaliza ceros que quedarían como -0.000000."""
        matriz = np.array(matriz, dtype=float, copy=True)
        umbral_visual = 0.5 * 10 ** (-precision)
        matriz[np.abs(matriz) <= umbral_visual] = 0.0

        def formato_float(valor):
            if abs(valor) <= umbral_visual:
                return "0"
            return f"{valor:.{precision}f}".rstrip("0").rstrip(".")

        return np.array2string(
            matriz,
            precision=precision,
            suppress_small=True,
            formatter={"float_kind": formato_float},
        )

    aumentada = np.column_stack((A, b))
    escala = max(1.0, float(np.linalg.norm(A, ord=np.inf)))
    umbral = tolerancia * escala

    print("\n" + "="*50)
    print("1. MATRIZ AMPLIADA INICIAL")
    print("="*50)
    print(matriz_a_texto(aumentada))

    # Eliminación hacia adelante (hasta la penúltima columna)
    for columna in range(n - 1):
        print(f"\n-ELIMINACIÓN: COLUMNA {columna + 1}-")
        
        # Verificación y selección del pivote
        if abs(aumentada[columna, columna]) <= umbral:
            fila_intercambio = -1
            for fila in range(columna + 1, n):
                if abs(aumentada[fila, columna]) > umbral:
                    fila_intercambio = fila
                    break
            
            if fila_intercambio != -1:
                aumentada[[columna, fila_intercambio]] = aumentada[[fila_intercambio, columna]]
                print(f"Se cambiaron las filas {columna + 1} y {fila_intercambio + 1} porque el valor de la fila {columna + 1} en esta columna era 0.")
                print("Matriz ampliada tras el intercambio:")
                print(matriz_a_texto(aumentada))
            else:
                print(f"¡Atención! Todos los valores disponibles en la columna {columna + 1} son 0.")
                print("El sistema no tiene una solución única (se evitará dividir por cero).")
                raise SistemaSingularError("Sistema singular detectado por columna nula.")

        valor_pivote = redondear(aumentada[columna, columna])
        print(f"Pivote elegido: fila {columna + 1}, columna {columna + 1}, valor = {formatear_numero(valor_pivote)}")
        
        hubo_operacion = False
        for fila in range(columna + 1, n):
            if abs(aumentada[fila, columna]) > umbral:
                factor = redondear(aumentada[fila, columna] / aumentada[columna, columna])
                print(f"Operación: Fila {fila + 1} = Fila {fila + 1} - ({formatear_numero(factor)}) * Fila {columna + 1}")
                
                for j in range(columna + 1, n + 1):
                    producto = redondear(factor * aumentada[columna, j])
                    aumentada[fila, j] = redondear(aumentada[fila, j] - producto)
                aumentada[fila, columna] = 0.0
                hubo_operacion = True

        if hubo_operacion:
            print("Matriz ampliada resultante después de las operaciones:")
            print(matriz_a_texto(aumentada))
        else:
            print("No se requirieron operaciones para anular los elementos debajo del pivote.")

    # Verificación final para el último elemento de la diagonal
    if abs(aumentada[n - 1, n - 1]) <= umbral:
        raise SistemaSingularError("El sistema es singular o casi singular: el último pivote es nulo.")

    print("\n" + "*"*50)
    print("2. MATRIZ TRIANGULAR SUPERIOR OBTENIDA")
    print("*"*50)
    print(matriz_a_texto(aumentada))

    print("\n" + "*"*50)
    print("3. SUSTITUCIÓN HACIA ATRÁS")
    print("*"*50)
    x = np.zeros(n, dtype=float)
    for fila in range(n - 1, -1, -1):
        resto = 0.0
        terminos_str = []
        for j in range(fila + 1, n):
            valor_producto = redondear(aumentada[fila, j] * x[j])
            resto = redondear(resto + valor_producto)
            terminos_str.append(f"({formatear_numero(redondear(aumentada[fila, j]))} * {formatear_numero(redondear(x[j]))})")
        
        x[fila] = redondear((aumentada[fila, n] - resto) / aumentada[fila, fila])
        
        lado_izquierdo = f"x{fila + 1}"
        if terminos_str:
            ecuacion = f"[{formatear_numero(redondear(aumentada[fila, n]))} - ({' + '.join(terminos_str)})] / {formatear_numero(redondear(aumentada[fila, fila]))}"
        else:
            ecuacion = f"{formatear_numero(redondear(aumentada[fila, n]))} / {formatear_numero(redondear(aumentada[fila, fila]))}"
            
        print(f"Cálculo de {lado_izquierdo}:")
        print(f"  {lado_izquierdo} = {ecuacion}")
        print(f"  {lado_izquierdo} = {formatear_numero(x[fila])}\n")

    print("*"*50)
    print("4. VALORES FINALES OBTENIDOS PARA LAS INCÓGNITAS")
    print("*"*50)
    for i in range(n):
        print(f"x_{i + 1} = {formatear_numero(x[i])}")

    return x, aumentada