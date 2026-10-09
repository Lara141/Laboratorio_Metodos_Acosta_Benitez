import math
import time

# Coeficientes del polinomio 3x^2 + 2x - 1 = 0
a = 3.0
b = 2.0
c = -1.0

inicio = time.perf_counter()
# Cálculo del discriminante
discriminante = (b**2) - (4 * a * c)
if discriminante >= 0:
    raiz_disc = math.sqrt(discriminante)
    
    # Control de estabilidad numérica (Cancelación por resta)
    if b > 0:
        raiz1 = (-2 * c) / (b + raiz_disc)
        raiz2 = (-b - raiz_disc) / (2 * a)
    else:
        raiz1 = (-b + raiz_disc) / (2 * a)
        raiz2 = (-2 * c) / (-b + raiz_disc)
        
    print(f"El valor de x1 es: {raiz1}")
    print(f"El valor de x2 es: {raiz2}")
else:
    print("La ecuación no tiene raíces reales.")
fin = time.perf_counter()
print(f"\nTiempo de ejecución: {fin - inicio:.6f} segundos")