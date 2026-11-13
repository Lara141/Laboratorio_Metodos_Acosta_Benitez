import numpy as np
from entrada import leer_float, leer_opcion_sn

def evaluar_polinomio(coeficientes, x):
    return np.polyval(coeficientes, x)

def ejecutar_biseccion(coeficientes):
    print("\n--- Método de Bisección ---")
    while True:
        a = leer_float("Ingresá el extremo inicial del intervalo (a): ")
        b = leer_float("Ingresá el extremo final del intervalo (b): ")
        if a >= b:
            print("Error: 'a' debe ser menor estricto que 'b'.")
            continue
        
        fa = evaluar_polinomio(coeficientes, a)
        fb = evaluar_polinomio(coeficientes, b)
        
        if fa * fb > 0:
            print(f"Error: p(a) = {fa:.4g} y p(b) = {fb:.4g} tienen el mismo signo. No se cumple la condición del teorema de Bolzano para aplicar bisección.")
            if leer_opcion_sn("¿Querés probar con otro intervalo? (s/n): ") != 's':
                return None
            continue
        break
            
    tol = 0.0001
    iteracion = 1
    error = abs(b - a)
    c_prev = a
    
    print(f"\nAplicando bisección en [{a}, {b}] con tolerancia < {tol}")
    print(f"{'Iter':<5} | {'a':<10} | {'b':<10} | {'c (medio)':<10} | {'p(c)':<12} | {'Error':<10}")
    print("-" * 65)
    
    while True:
        c = (a + b) / 2
        fc = evaluar_polinomio(coeficientes, c)
        error = abs(c - c_prev)
        
        print(f"{iteracion:<5} | {a:<10.5g} | {b:<10.5g} | {c:<10.5g} | {fc:<12.5g} | {error:<10.5g}")
        
        if abs(fc) < 1e-10 or (iteracion > 1 and error < tol):
            print("-" * 65)
            print(f"Raíz aproximada encontrada: λ = {c:.6g}")
            print(f"Criterio de parada alcanzado (Error < {tol} o p(c) ≈ 0).")
            return c
            
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
            
        c_prev = c
        iteracion += 1