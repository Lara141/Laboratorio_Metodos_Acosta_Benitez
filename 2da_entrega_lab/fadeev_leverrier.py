#Cálculo de autovalores mediante el método de Fadeev LeVerrier.
#Este módulo desarrolla la construcción del polinomio característico a partir de
#las trazas de matrices auxiliares y muestra cómo obtener un vector propio asociado
#para un autovalor dado mediante eliminación gaussiana.

import numpy as np


def fmt(val, tol=1e-10):
    # Formatea un valor numérico para mostrarlo en consola.
    # Convierte explícitamente a float nativo para evitar representaciones como np.float64(...)
    val_float = float(val)
    
    # Convierte valores cercanos a cero en '0' para mejorar la legibilidad y evitar '-0' o '-0.0'
    if abs(val_float) < tol:
        return "0"
        
    # El formato :g elimina automáticamente los ceros no significativos y el punto 
    # decimal en números enteros (ej: 3.0 -> 3, 3.25 -> 3.25)
    return f"{val_float:g}"

def format_array(arr):
    # Función auxiliar para aplicar el formato uniformemente a matrices y vectores.
    # El parámetro 'formatter' delega la impresión de cada número a nuestra función fmt.
    return np.array2string(arr, formatter={'float_kind': lambda x: fmt(x)})


def calcular_fadeev(A: np.ndarray):
    #Calcula el polinomio característico y los coeficientes del método.
    #Args:
      #  A: Matriz cuadrada sobre la que se desea calcular el espectro.
    #Returns:
      #  Tupla (b_k_list, coeficientes, polinomio_str) con los coeficientes
      # intermedios, los coeficientes del polinomio y su representación textual.
    
    n = A.shape[0]
    identidad = np.eye(n)

    print("MÉTODO DE FADEEV-LEVERRIER")
    print("-"*50)

    B = A.copy()
    print("1. B_1 = A =\n", format_array(B))

    b_1 = np.trace(B)
    b_k_list = [b_1]

    suma_traza = " + ".join([fmt(x) for x in np.diag(B)])
    print(f"\nb_1 = tr(B_1) = {suma_traza} = {fmt(b_1)}")

    for k in range(2, n + 1):
        print(f"\nIteración k = {k}")
        B_prev = B.copy()
        b_prev = b_k_list[-1]

        bI = b_prev * identidad
        resta = B_prev - bI

        print(f"Fórmula: B_{k} = A * (B_{k-1} - b_{k-1}I)")
        print(f"\nb_{k-1}I =\n", format_array(bI))
        print(f"\n(B_{k-1} - b_{k-1}I) =\n", format_array(resta))

        B = A @ resta
        print(f"\nB_{k} =\n", format_array(B))

        tr_B = np.trace(B)
        b_k = tr_B / k
        b_k_list.append(b_k)

        suma_traza = " + ".join([fmt(x) for x in np.diag(B)])
        print(f"b_{k} = (1/{k}) * tr(B_{k}) = (1/{k}) * ({suma_traza}) = {fmt(b_k)}")

    coeficientes = [1.0]
    for b in b_k_list:
        coeficientes.append(-b)

    print("\n")
    print("POLINOMIO CARACTERÍSTICO")
    print("-"*50)
    terminos = [f"λ^{n}"]
    for i, b in enumerate(b_k_list, 1):
        pot = n - i
        lam_str = f"λ^{pot}" if pot > 1 else ("λ" if pot == 1 else "")
        
        # Limpiamos el valor para el signo y para evitar arrastrar un -0 a la impresión
        b_float = float(b)
        if abs(b_float) < 1e-10:
            b_float = 0.0
            
        signo = "+" if -b_float >= 0 else "-"
        terminos.append(f" {signo} {fmt(abs(b_float))}{lam_str}")

    polinomio_str = "".join(terminos)
    if polinomio_str.startswith(" + "):
        polinomio_str = polinomio_str[3:]
    print(f"p(λ) = {polinomio_str} = 0")

    return b_k_list, coeficientes, polinomio_str


def calcular_autovector(A, lambd, tolerancia=1e-5):
    #Obtiene un autovector asociado al autovalor dado usando Gauss.
    # Args:
    # A: Matriz cuadrada.
    # lambd: Valor propio para el cual se busca el vector asociado.
    # tolerancia: Umbral para considerar un valor casi nulo.
    #Returns:
     #   Vector propio aproximado asociado a lambd.
    
    n = A.shape[0]
    identidad = np.eye(n)

    print(f"Cálculo de autovector para λ = {fmt(lambd)}")
    print("-" * 40)

    M = A - lambd * identidad
    print(f"Sistema homogéneo (A - λI)v = 0\nMatriz (A - {fmt(lambd)}I):")
    print(format_array(M))

    print("\nAplicando eliminación de Gauss por filas:")
    M_gauss = M.copy()
    for col in range(n - 1):
        max_idx = col + np.argmax(np.abs(M_gauss[col:, col]))
        if np.abs(M_gauss[max_idx, col]) > tolerancia:
            if max_idx != col:
                M_gauss[[col, max_idx]] = M_gauss[[max_idx, col]]
                print(f"Intercambio Fila {col+1} y Fila {max_idx+1}")
            for row in range(col + 1, n):
                if np.abs(M_gauss[row, col]) > tolerancia:
                    factor = M_gauss[row, col] / M_gauss[col, col]
                    M_gauss[row, col:] -= factor * M_gauss[col, col:]
                    print(f"-> Fila {row+1} = Fila {row+1} - ({fmt(factor)}) * Fila {col+1}")

    print("\nMatriz escalonada:")
    print(format_array(M_gauss))

    v = np.zeros(n)
    v[-1] = 1.0
    print(f"\nAl ser un sistema dependiente, tomamos la variable libre v_{n} = 1")

    for row in range(n - 2, -1, -1):
        if np.abs(M_gauss[row, row]) > tolerancia:
            suma = sum(M_gauss[row, c] * v[c] for c in range(row + 1, n))
            v[row] = -suma / M_gauss[row, row]
        else:
            v[row] = 1.0

    print("Vector asociado resultante v =")
    print(format_array(v))

    Av = A @ v
    lv = lambd * v
    print(f"\nComprobación:")
    print(f"A * v = {format_array(Av)}")
    print(f"λ * v = {format_array(lv)}")

    return v