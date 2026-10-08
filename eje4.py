import time

inicio = time.perf_counter()


a=3
b=2
c=-1
discriminante = (b**2)-(4*a*c)

if discriminante >=0:
    x1= float((-b + (discriminante**0.5)) /(2*a))
    x2= float((-b - (discriminante**0.5)) /(2*a))

    print("los valores de x son: x1:", x1, "x2:", x2)
else:
    print("no se encontro solucion")


fin = time.perf_counter()

tiempo_total = fin - inicio
print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")