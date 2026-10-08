import math
import time

#Hacerlo Dinamico
 
#Funciones 
#simula la aritmética de la computadora redondeando a un número fijo de cifras significativas
def fl(valor, cifras_sig=3):
    # Si el valor es exactamente 0, se devuelve 0.0 para evitar errores matemáticos con logaritmos
    if valor == 0:
        return 0.0
    
    # math.log10(abs(valor)) obtiene el exponente decimal del número. 
    # math.floor() lo redondea hacia abajo para encontrar su magnitud real
    magnitud = math.floor(math.log10(abs(valor)))
    
    # La cantidad de decimales a redondear se calcula restando la magnitud a las cifras significativas - 1.
    valor_redondeado = round(valor, cifras_sig - 1 - magnitud)
    
    return valor_redondeado

#calculamos los errores absolutos y relativos entre el valor exacto y el aproximado
def errores(exacto, aprox):
   
    # Error Absoluto = |Valor Exacto - Valor Aproximado|
    e_abs = abs(exacto - aprox)
    
    # Error Relativo = Error Absoluto / |Valor Exacto| (evitando división por cero)
    e_rel = e_abs / abs(exacto) if exacto != 0 else 0
    
    return e_abs, e_rel

start_time = time.perf_counter()
# resolvemos cada uno de los puntos del ejercicio
#valor = float(input("Ingrese el valor de p: "))

#exacto_i=round(valor, 5) # Calculamos el valor exacto redondeado a 5 decimales
#aprox_i = fl(valor) # Simulamos la aritmética de la computadora redondeando el valor ingresado


# punto a
exacto_a = round(133 + 0.921, 5) # Calculamos el valor exacto redondeado a 5 decimales
# Simulamos la aritmética de la computadora redondeando cada operando y luego el resultado de la suma
aprox_a = fl(fl(133) + fl(0.921)) 
eAbs_a, eRel_a = errores(exacto_a, aprox_a) # obtengo el error absoluto y el error relativo

# punto b
exacto_b = round(133 - 0.499, 5) 
aprox_b = fl(fl(133) - fl(0.499)) 
eAbs_b, eRel_b = errores(exacto_b, aprox_b)

# punto c
exacto_c = round((121 - 119) - 0.327, 5)
# El cálculo se realiza respetando los paréntesis, aplicando la normalización en cada paso individual
paso1_c = fl(fl(121) - fl(119))
aprox_c = fl(paso1_c - fl(0.327))
eAbs_c, eRel_c = errores(exacto_c, aprox_c)

# punto d
exacto_d = round((121 - 0.327) - 119, 5)
paso1_d = fl(fl(121) - fl(0.327))
aprox_d = fl(paso1_d - fl(119))
eAbs_d, eRel_d = errores(exacto_d, aprox_d)

# punto e
exacto_e = round((2/9) * (9/7), 5)
# Cada división se calcula de forma independiente normalizando numerador y denominador, luego sus cocientes, y finalmente el producto
paso1_e = fl(fl(2) / fl(9))
paso2_e = fl(fl(9) / fl(7))
aprox_e = fl(paso1_e * paso2_e)
eAbs_e, eRel_e = errores(exacto_e, aprox_e)

end_time = time.perf_counter()
tiempo_ejecucion = end_time - start_time

#muestra los resultados por pantalla
print(f"a. Resultado de 133 + 0.921 (valor exacto): {exacto_a:.5f} | Aproximado : {aprox_a} | E. Absoluto: |{exacto_a:.5f} - {aprox_a}| = {eAbs_a} | E. Relativo :  {eAbs_a} / |{exacto_a:.5g}| =  {eRel_a}")
print(f"b. Resultado de 133 - 0.499 (valor exacto): {exacto_b:.5f} | Aproximado: {aprox_b} | E. Absoluto: | {exacto_b:.5f} - {aprox_b}| = {eAbs_b} | E. Relativo :  {eAbs_b} / |{exacto_b:.5g}| =  {eRel_b}")
print(f"c. Resultado de (121 - 119) - 0.327 (valor exacto): {exacto_c:.5f} | Aproximado: {aprox_c} | E. Absoluto: |{exacto_c:.5f} - {aprox_c}| = {eAbs_c} | E. Relativo :  {eAbs_c} / |{exacto_c:.5g}| =  {eRel_c}")
print(f"d. Resultado de (121 - 0.327) - 119 (valor exacto): {exacto_d:.5f} | Aproximado: {aprox_d} | E. Absoluto: |{exacto_d:.5f} - {aprox_d}| = {eAbs_d} | E. Relativo :  {eAbs_d} / |{exacto_d:.5g}| =  {eRel_d}")
print(f"e. Resultado de (2/9) * (9/7) (valor exacto): {exacto_e:.5f} | Aproximado: {aprox_e} | E. Absoluto: |{exacto_e:.5f} - {aprox_e}| = {eAbs_e:.5g} | E. Relativo :  {eAbs_e} / |{exacto_e:.5g}| =  {eRel_e}")

print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")