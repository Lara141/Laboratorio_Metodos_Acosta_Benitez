import random
import time

n = int(input("Ingrese la cantidad de números a sumar (N): "))

print("Números generados:")
tiempo_inicio = time.time()

total = 0
for i in range(1, n + 1):
    numero = random.randint(0, 255)
    print(numero, end=" ")
    total = total + numero

print("\n") 

tiempo_fin = time.time()
tiempo_total = tiempo_fin - tiempo_inicio

print(f"Suma total de los valores: {total}")
print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")