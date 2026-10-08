import math
import time

# Función para truncar o redondear un número a un número específico de cifras significativas
def cifra_sig(valor, cifras=3, modo="redondeo"):
    if valor == 0:
        return 0.0
    magnitud = math.floor(math.log10(abs(valor)))
    factor = 10 ** (cifras - 1 - magnitud)
    if modo == "truncamiento":
        return math.trunc(valor * factor) / factor
    else:
        return round(valor, cifras - 1 - magnitud)


start_time = time.perf_counter()

# Valor inicial
x = 4.71

# calculo el valor exacto de la funcion
x2_ex = x * x
x3_ex = x2_ex * x
t2_ex = 6 * x2_ex
t3_ex = 3 * x
f_ex = x3_ex - t2_ex + t3_ex - 0.149

# calculo con truncamiento
x2_tr = cifra_sig(x * x, 3, "truncamiento")
x3_tr = cifra_sig(x2_tr * x, 3, "truncamiento")
t2_tr = cifra_sig(6 * x2_tr, 3, "truncamiento")
t3_tr = cifra_sig(3 * x, 3, "truncamiento")

suma1_tr = cifra_sig(x3_tr - t2_tr, 3, "truncamiento")
suma2_tr = cifra_sig(suma1_tr + t3_tr, 3, "truncamiento")
f_tr = cifra_sig(suma2_tr - 0.149, 3, "truncamiento")

# calculo com redondeo
x2_re = cifra_sig(x * x, 3, "redondeo")
x3_re = cifra_sig(x2_re * x, 3, "redondeo")
t2_re = cifra_sig(6 * x2_re, 3, "redondeo")
t3_re = cifra_sig(3 * x, 3, "redondeo")

suma1_re = cifra_sig(x3_re - t2_re, 3, "redondeo")
suma2_re = cifra_sig(suma1_re + t3_re, 3, "redondeo")
f_re = cifra_sig(suma2_re - 0.149, 3, "redondeo")

# 4. ERRORES
e_abs_tr = abs(f_ex - f_tr)
e_rel_tr = e_abs_tr / abs(f_ex)

e_abs_re = abs(f_ex - f_re)
e_rel_re = e_abs_re / abs(f_ex)

end_time = time.perf_counter()
tiempo_ejecucion = end_time - start_time

# mostramos los resultados por pantalla como una tabla
print("-" * 88)
print(f"| {'Modo':<28} | {'X':<6} | {'X^2':<10} | {'X^3':<10} | {'6x^2':<10} | {'3x':<6} |")
print("-" * 88)
print(f"| {'Exacto':<28} | {x:<6} | {x2_ex:<10.6f} | {x3_ex:<10.6f} | {t2_ex:<10.4f} | {t3_ex:<6.2f} |")
print(f"| {'Tres dígitos (truncados)':<28} | {x:<6} | {x2_tr:<10.1f} | {x3_tr:<10.1f} | {t2_tr:<10.1f} | {t3_tr:<6.1f} |")
print(f"| {'Tres dígitos (redondeados)':<28} | {x:<6} | {x2_re:<10.1f} | {x3_re:<10.1f} | {t2_re:<10.1f} | {t3_re:<6.1f} |")
print("-" * 88)

print(f"\nf(4.71) Exacto     = {f_ex:.6f}")
print(f"f(4.71) Truncado   = {f_tr} -> Error Absoluto = {e_abs_tr:.6f}, Error Relativo = {e_rel_tr:.9f}")
print(f"f(4.71) Redondeado = {f_re} -> Error Absoluto = {e_abs_re:.6f}, Error Relativo = {e_rel_re:.9f}")
print("-" * 88)
print(f"Tiempo de ejecución computacional: {tiempo_ejecucion:.8f} segundos")