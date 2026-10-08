import time

inicio = time.perf_counter()

aprox_e = 0
factorial = 1
n = int(input("Ingrese la cantidad de numeros que quiere sumar para la precision: "))

for i in range(n):
    if i > 0:
        factorial = factorial * i
    
    termino = 1 / factorial
    aprox_e = aprox_e + termino
    print(f"Iteración {i} (1/{i}!): se sumó {termino} -valor aproximado de e: {aprox_e}")

fin = time.perf_counter()
tiempo_ejecucion = fin - inicio

print("\nEl valor aproximado de e con", n, "sumandos es:", aprox_e)
print(f"Tiempo de ejecucion: {tiempo_ejecucion:.6f} segundos")