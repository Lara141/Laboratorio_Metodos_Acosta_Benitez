import math
import time

n = int(input("ingrese la cantidad de cifras decimales exactas: "))
inicio = time.process_time()

pi_truncado = int(math.pi * (10 ** n))

S_N = 0
k = 0
signo = 1

while True:
    termino = signo * (4 / (2 * k + 1))
    S_N = S_N + termino
    k = k + 1
    signo = -signo
    if int(S_N * (10 ** n)) == pi_truncado:
        break

fin = time.process_time()
tiempo = fin - inicio
aprox_mostrar = int(S_N * (10 ** n)) / (10 ** n)

print(f"aproximacion de pi con {n} cifras decimales: {aprox_mostrar:.15f}")
print(f"cantidad de terminos necesarios: {k}")
print(f"tiempo: {tiempo:.6f}")