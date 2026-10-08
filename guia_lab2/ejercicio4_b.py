import math
import time 

inicio = time.perf_counter()

def redondear4(numero):
    if numero == 0:
        return 0
    return round(numero, 3 - int(math.floor(math.log10(abs(numero)))))

# Datos
a = 1
b = 62.10
c = 1

# Valores dados por el ejercicio
x1_exacto = -0.01610723
x2_exacto = -62.08390

# Discriminante
b_cuadrado = redondear4(b * b)
cuatro_ac = redondear4(4 * a * c)

discriminante = redondear4(b_cuadrado - cuatro_ac)
raiz_discriminante = redondear4(math.sqrt(discriminante))

# Fórmulas racionalizadas
numerador = redondear4(2 * c)

denominador_x1 = redondear4(-b - raiz_discriminante)
x1 = redondear4(numerador / denominador_x1)

denominador_x2 = redondear4(-b + raiz_discriminante)
x2 = redondear4(numerador / denominador_x2)

# Errores
error_abs_x1 = abs(x1_exacto - x1)
error_rel_x1 = error_abs_x1 / abs(x1_exacto)

error_abs_x2 = abs(x2_exacto - x2)
error_rel_x2 = error_abs_x2 / abs(x2_exacto)

#Tiempo de ejecución
fin = time.perf_counter()
tiempo_total = fin - inicio

# Resultados
print("x1 racionalizada =", x1)
print("Error absoluto x1 =", error_abs_x1)
print("Error relativo x1 =", error_rel_x1)

print("\nx2 racionalizada =", x2)
print("Error absoluto x2 =", error_abs_x2)
print("Error relativo x2 =", error_rel_x2)

print(f"\nTiempo de ejecución: {tiempo_total:.6f} segundos")