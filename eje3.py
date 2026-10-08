import time

a = 0
b = 1
contador = 1
posicion_sig = 0

n = int(input("Ingrese la cantidad N de términos de Fibonacci: "))

inicio = time.perf_counter()

if n >= 1:
    print(a, end="") 
    contador = contador + 1

if n >= 2:
    print(f" - {b}", end="")
    contador = contador + 1

while contador <= n:
    posicion_sig = a + b
    print(f" - {posicion_sig}", end="") 
    
    a = b
    b = posicion_sig
    contador = contador + 1

fin = time.perf_counter()
tiempo_total = fin - inicio

print(f"\n\nTiempo de ejecución: {tiempo_total:.6f} segundos")