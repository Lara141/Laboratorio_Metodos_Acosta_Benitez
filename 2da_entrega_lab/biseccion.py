#Implementación del método de bisección para hallar raíces reales de un polinomio.
#Este módulo permite aproximar una raíz de p(x) = 0 en un intervalo [a, b] donde
#la función cambia de signo, garantizando la convergencia bajo la condición de Bolzano

import numpy as np
from entrada import leer_float, leer_opcion_sn


def evaluar_polinomio(coeficientes, x):
    #Evalúa un polinomio en un punto dado usando la convención de NumPy.

    #Args:
    #   coeficientes: Coeficientes del polinomio en orden descendente de potencia.
    #    x: Punto donde se evalúa el polinomio.

    #Returns:
    #    Valor numérico del polinomio en x.
    
    return np.polyval(coeficientes, x)


def ejecutar_biseccion(coeficientes):
   
   #Ejecuta la bisección para encontrar una raíz de un polinomio.
    #El algoritmo valida que exista un cambio de signo en el intervalo ingresado,
    #reduce iterativamente el intervalo a la mitad y devuelve la raíz aproximada
    #cuando se cumple el criterio de tolerancia.

    #Args:
     #   coeficientes: Coeficientes del polinomio a resolver.

    #Returns:
     #   La raíz aproximada encontrada o None si el usuario cancela o el intervalo
      #  no cumple la hipótesis del teorema de Bolzano.

    print("\nMétodo de Bisección")
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