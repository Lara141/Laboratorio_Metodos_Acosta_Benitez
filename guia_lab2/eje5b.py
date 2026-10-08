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

x = 4.71

# valor exacto de la funcion
# f(x) = ((x - 6)x + 3)x - 0.149
f_ex = ((x - 6) * x + 3) * x - 0.149

# calculo los truncamientos
paso1_tr = cifra_sig(x - 6, 3, "truncamiento")         # 4.71 - 6 = -1.29
paso2_tr = cifra_sig(paso1_tr * x, 3, "truncamiento")  # -1.29 * 4.71 = -6.07
paso3_tr = cifra_sig(paso2_tr + 3, 3, "truncamiento")  # -6.07 + 3 = -3.07
paso4_tr = cifra_sig(paso3_tr * x, 3, "truncamiento")  # -3.07 * 4.71 = -14.4
f_tr = cifra_sig(paso4_tr - 0.149, 3, "truncamiento")  # -14.4 - 0.149 = -14.5

# calculo los redondeos
paso1_re = cifra_sig(x - 6, 3, "redondeo")             # 4.71 - 6 = -1.29
paso2_re = cifra_sig(paso1_re * x, 3, "redondeo")      # -1.29 * 4.71 = -6.08
paso3_re = cifra_sig(paso2_re + 3, 3, "redondeo")      # -6.08 + 3 = -3.08
paso4_re = cifra_sig(paso3_re * x, 3, "redondeo")      # -3.08 * 4.71 = -14.5
f_re = cifra_sig(paso4_re - 0.149, 3, "redondeo")      # -14.5 - 0.149 = -14.6

# calculo los errores absolutos y relativos
e_abs_tr = abs(f_ex - f_tr)
e_rel_tr = e_abs_tr / abs(f_ex)

e_abs_re = abs(f_ex - f_re)
e_rel_re = e_abs_re / abs(f_ex)

end_time = time.perf_counter()
tiempo_ejecucion = end_time - start_time

# mostramos los resultados por pantalla
print("-" * 85)
print(f"| {'Método':<25} | {'Resultado f(4.71)':<20} | {'E. Absoluto':<15} | {'E. Relativo':<15} |")
print("-" * 85)
print(f"| {'Exacto':<25} | {f_ex:<20.6f} | {'-':<15} | {'-':<15} |")
print(f"| {'Anidado (Truncamiento)':<25} | {f_tr:<20.1f} | {e_abs_tr:<15.6f} | {e_rel_tr:<15.5f} |")
print(f"| {'Anidado (Redondeo)':<25} | {f_re:<20.1f} | {e_abs_re:<15.6f} | {e_rel_re:<15.5f} |")
print("-" * 85)
print(f"\nTiempo de ejecución computacional: {tiempo_ejecucion:.8f} segundos")