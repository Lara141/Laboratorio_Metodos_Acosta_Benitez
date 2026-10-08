import math
import time

#simula la aritmética de la computadora redondeando a un número fijo de cifras significativas
def fl_trunc(valor, cifras_sig=3):
    if valor == 0:
        return 0.0
    
    # Obtenemos la magnitud del número
    magnitud = math.floor(math.log10(abs(valor)))
    
    # Calculamos el factor de desplazamiento para las cifras significativas
    factor = 10 ** (cifras_sig - 1 - magnitud)
    
    # Multiplicamos, usamos math.trunc para cortar, y dividimos
    return math.trunc(valor * factor) / factor

#calculamos los errores absolutos y relativos entre el valor exacto y el aproximado
def errores(exacto, aprox):
    
    e_abs = abs(exacto - aprox)
    e_rel = e_abs / abs(exacto) if exacto != 0 else 0
    return e_abs, e_rel


start_time = time.perf_counter()

# punto a
exacto_a = round(133 + 0.921, 5) 
aprox_a = fl_trunc(fl_trunc(133) + fl_trunc(0.921)) 
eAbs_a, eRel_a = errores(exacto_a, aprox_a) 

# punto b
exacto_b = round(133 - 0.499, 5) 
aprox_b = fl_trunc(fl_trunc(133) - fl_trunc(0.499)) 
eAbs_b, eRel_b = errores(exacto_b, aprox_b)

# punto c
exacto_c = round((121 - 119) - 0.327, 5)
paso1_c = fl_trunc(fl_trunc(121) - fl_trunc(119))
aprox_c = fl_trunc(paso1_c - fl_trunc(0.327))
eAbs_c, eRel_c = errores(exacto_c, aprox_c)

# punto d
exacto_d = round((121 - 0.327) - 119, 5)
paso1_d = fl_trunc(fl_trunc(121) - fl_trunc(0.327))
aprox_d = fl_trunc(paso1_d - fl_trunc(119))
eAbs_d, eRel_d = errores(exacto_d, aprox_d)

# punto e
exacto_e = round((2/9) * (9/7), 5)
paso1_e = fl_trunc(fl_trunc(2) / fl_trunc(9))
paso2_e = fl_trunc(fl_trunc(9) / fl_trunc(7))
aprox_e = fl_trunc(paso1_e * paso2_e)
eAbs_e, eRel_e = errores(exacto_e, aprox_e)

end_time = time.perf_counter()
tiempo_ejecucion = end_time - start_time

#muestro los resultados por pantalla
print(f"a. Resultado de 133 + 0.921 (valor exacto): {exacto_a:.5f} | Aproximado : {aprox_a} | E. Absoluto: |{exacto_a:.5g} - {aprox_a:.5f}| = {eAbs_a:.5f} | E. Relativo :  {eAbs_a:.5f} / |{exacto_a:.5g}| =  {eRel_a:.5f}")
print(f"b. Resultado de 133 - 0.499 (valor exacto): {exacto_b:.5f} | Aproximado: {aprox_b} | E. Absoluto: | {exacto_b:.5f} - {aprox_b:.5f}| = {eAbs_b:.5f} | E. Relativo :  {eAbs_b:.5f} / |{exacto_b:.5g}| =  {eRel_b:.5f}")
print(f"c. Resultado de (121 - 119) - 0.327 (valor exacto): {exacto_c:.5f} | Aproximado: {aprox_c} | E. Absoluto: |{exacto_c:.5f} - {aprox_c:.5f}| = {eAbs_c:.5f} | E. Relativo :  {eAbs_c:.5f} / |{exacto_c:.5g}| =  {eRel_c:.5f}")
print(f"d. Resultado de (121 - 0.327) - 119 (valor exacto): {exacto_d:.5f} | Aproximado: {aprox_d} | E. Absoluto: |{exacto_d:.5f} - {aprox_d:.5f}| = {eAbs_d:.5f} | E. Relativo :  {eAbs_d:.5f} / |{exacto_d:.5g}| =  {eRel_d:.5f}")
print(f"e. Resultado de (2/9) * (9/7) (valor exacto): {exacto_e:.5f} | Aproximado: {aprox_e} | E. Absoluto: |{exacto_e:.5f} - {aprox_e:.5f}| = {eAbs_e:.5f} | E. Relativo :  {eAbs_e:.5f} / |{exacto_e:.5g}| =  {eRel_e:.5f}")

print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")