import math
import time 

inicio = time.perf_counter()

def calcular_error(p, pAprox):
    errorAbsoluto = abs(p - pAprox)
    errorRelativo = errorAbsoluto / abs(p)
    
    print("Error absoluto: ", errorAbsoluto)
    print("Error relativo: ", errorRelativo)

print("a)")
calcular_error(math.pi, 22/7)

print("\nb)")
calcular_error(math.pi, 3.1416)

print("\nc)")
calcular_error(math.e, 2.718)

print("\nd)")
calcular_error(math.sqrt(2), 1.414)

print("\ne)")
calcular_error(math.exp(10), 22000)

print("\nf)")
calcular_error(math.factorial(8), 39900)


fin = time.perf_counter()
tiempo_total = fin - inicio
print(f"\nTiempo de ejecución: {tiempo_total:.6f} segundos")