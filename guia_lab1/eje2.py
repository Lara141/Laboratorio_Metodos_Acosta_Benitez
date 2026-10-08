
import random
import time

n = 200
total = 0

print(f"Generando {n} números aleatorios...")
inicio = time.perf_counter()

for i in range(1, n + 1):
    numero = random.randint(0, 255)
    print(numero, end=" ")
    if numero % 2 == 0:
        total = total + numero

print("\n") 

fin = time.perf_counter()
tiempo_total = fin - inicio

print(f"La suma total de los números PARES es: {total}")
print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")