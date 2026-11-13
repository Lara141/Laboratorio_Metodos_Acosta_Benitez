#Programa principal de la segunda entrega del laboratorio.
#Integra distintos métodos numéricos: análisis de signos de Descartes, búsqueda de
#raíces por tanteo y bisección, cálculo de autovalores y resolución de integrales.
import time
import numpy as np
from entrada import ingresar_sistema, leer_float, leer_opcion_sn, leer_opcion_menu
from fadeev_leverrier import calcular_fadeev, calcular_autovector
from descartes import analisis_descartes
from biseccion import evaluar_polinomio, ejecutar_biseccion
from trapecios import ejecutar_trapecios

def busqueda_autovalores(coeficientes, n):
#Busca raíces reales de un polinomio usando Descartes y bisección.
    max_pos, max_neg = analisis_descartes(coeficientes)
    raices_encontradas = []
    
    busco_negativos = False
    busco_positivos = False

    while True:
        pendientes_pos = len([r for r in raices_encontradas if r > 0]) < max_pos
        pendientes_neg = len([r for r in raices_encontradas if r < 0]) < max_neg

        # Mensaje predeterminado
        mensaje_tanteo = "\n¿Querés tantear raíces reales en un intervalo? (s/n): "
        
        # Ajuste dinámico de los mensajes luego de haber realizado al menos un tanteo
        if busco_positivos or busco_negativos:
            if not pendientes_pos and max_pos > 0 and pendientes_neg and max_neg > 0:
                mensaje_tanteo = "\nSe encontraron los autovalores positivos, pero todavía faltan buscar los negativos. ¿Desea aplicar tanteo para buscarlos? (s/n): "
            elif not pendientes_neg and max_neg > 0 and pendientes_pos and max_pos > 0:
                mensaje_tanteo = "\nSe encontraron los autovalores negativos, pero todavía faltan buscar los positivos. ¿Desea aplicar tanteo para buscarlos? (s/n): "
            elif not pendientes_pos and not pendientes_neg:
                mensaje_tanteo = "\nYa se encontraron todos los autovalores reales posibles según Descartes. ¿Querés realizar un nuevo tanteo de todas formas? (s/n): "

        resp = leer_opcion_sn(mensaje_tanteo)
        if resp != 's':
            break
            
        inicio = leer_float("Valor inicial del tanteo (-3): ")
        fin = leer_float("Valor final del tanteo (5): ")
        paso = leer_float("Incremento (1): ") 
        
        if inicio >= fin or paso <= 0:
            print("Error: El valor inicial debe ser menor al final y el incremento debe ser mayor a cero.")
            continue
            
        if inicio < 0 or fin < 0: busco_negativos = True
        if inicio > 0 or fin > 0: busco_positivos = True
            
        print("\nResultados del tanteo:")
        print(f"{'λ':<10} | {'p(λ)':<12}")
        print("-" * 25)
        
        valores = np.arange(inicio, fin + paso, paso)
        prev_y = None
        prev_x = None
        
        intervalos_cambio = []
        
        for x in valores:
            y = evaluar_polinomio(coeficientes, x)
            print(f"{x:<10.4g} | {y:<12.4g}")
            
            if abs(y) < 1e-10:
                raiz_nativa = float(x)
                if not any(abs(raiz_nativa - r) < 1e-3 for r in raices_encontradas):
                    print(f"*** Raíz exacta encontrada en λ = {raiz_nativa:.4g} ***")
                    raices_encontradas.append(raiz_nativa)
                    
            if prev_y is not None and abs(y) >= 1e-10 and np.sign(y) != np.sign(prev_y):
                intervalos_cambio.append((float(prev_x), float(x)))
                
            prev_x = x
            prev_y = y
            
        pos_halladas = len([r for r in raices_encontradas if r > 0])
        neg_halladas = len([r for r in raices_encontradas if r < 0])
        
        for a, b in intervalos_cambio:
            es_positivo = a >= 0 and b > 0
            
            if es_positivo and pos_halladas >= max_pos:
                continue
            if not es_positivo and neg_halladas >= max_neg:
                continue
                
            acc = leer_opcion_sn(f"\nPara el intervalo con cambio de signo [{a:.4g}, {b:.4g}], ¿querés aplicar bisección? (s/n): ")
            if acc == 's':
                raiz = ejecutar_biseccion(coeficientes)
                if raiz is not None:
                    raiz_nativa = float(raiz)
                    if not any(abs(raiz_nativa - r) < 1e-3 for r in raices_encontradas):
                        raices_encontradas.append(raiz_nativa)
                        if raiz_nativa > 0: pos_halladas += 1
                        else: neg_halladas += 1
                    else:
                        print("Esta raíz ya estaba en la lista.")

        faltan_pos = pos_halladas < max_pos
        faltan_neg = neg_halladas < max_neg
        
        if (faltan_pos or faltan_neg) and not intervalos_cambio:
            print("\nNo se detectaron intervalos con cambio de signo en este tanteo, pero Descartes indica que podrían existir más raíces.")
            print("Esto puede ocurrir porque el intervalo es incorrecto, el incremento es muy grande, o las raíces son repetidas/complejas.")
            print("Podés intentar repetir el tanteo con otros valores o un incremento menor.")
            
    raices_encontradas.sort()
    return raices_encontradas

def ejecutar_flujo_fadeev():
#Ejecuta el flujo completo del método de Fadeev Leverrier
    A = ingresar_sistema()
    n = A.shape[0]
    inicio = time.perf_counter()
    
    b_k_list, coeficientes, polinomio_str = calcular_fadeev(A)
    
    autovalores_reales = []
    if leer_opcion_sn("\n¿Querés buscar los autovalores? (s/n): ") == 's':
        autovalores_reales = busqueda_autovalores(coeficientes, n)
        
    raices_extra = []
    if len(autovalores_reales) < n:
        faltantes = n - len(autovalores_reales)
        print(f"\n¡Atención! La matriz es de orden {n}, por lo que el polinomio debe tener {n} raíces en total.")
        print(f"Se encontraron {len(autovalores_reales)} raíces mediante tanteo y bisección. Faltan {faltantes} raíces.")
        print("Estas raíces faltantes podrían ser autovalores múltiples (repetidos) o complejos (imaginarios), los cuales no se pueden detectar con bisección.")
        
        if leer_opcion_sn("¿Deseas calcular las raíces faltantes utilizando un método analítico automatizado? (s/n): ") == 's':
            todas_las_raices = np.roots(coeficientes)
            for r in todas_las_raices:
                es_real = abs(r.imag) < 1e-10
                r_val = float(r.real) if es_real else complex(r)
                ya_encontrada = es_real and any(abs(r_val - real_r) < 1e-3 for real_r in autovalores_reales)
                if not ya_encontrada:
                    raices_extra.append(r_val)

    autovectores_calculados = []
    if autovalores_reales:
        print("\nAutovalores reales listos para procesar:", [round(r, 6) for r in autovalores_reales])
        print("\n¿Qué deseas hacer con los autovectores?")
        print("1. Buscar los autovectores de TODOS los autovalores reales")
        print("2. Buscar UN SOLO autovector")
        print("3. Omitir y ver el resumen")
        
        opc_vec = leer_opcion_menu("Elegí una opción: ", ['1', '2', '3'])
        if opc_vec == '1':
            for lambd in autovalores_reales:
                v = calcular_autovector(A, lambd)
                autovectores_calculados.append((lambd, v))
        elif opc_vec == '2':
            val = leer_float("Ingresá el autovalor para calcular su autovector: ")
            match = [r for r in autovalores_reales if abs(r - val) < 1e-3]
            if match:
                lambd_real = match[0]
                print(f"Autovalor aceptado (aproximado a {lambd_real}).")
                v = calcular_autovector(A, lambd_real)
                autovectores_calculados.append((lambd_real, v))
            else:
                print("El valor ingresado no coincide con ninguna de las raíces reales encontradas iterativamente.")
    
    fin = time.perf_counter()
    
   
    print("RESULTADOS FINALES")
    print("-"*50)
    print("Valores b_k calculados:")
    for i, b in enumerate(b_k_list, 1):
        print(f"b_{i} = {b:g}")
        
    print(f"\nPolinomio característico:\np(λ) = {polinomio_str} = 0")
    
    print("\nAutovalores reales encontrados iterativamente:")
    if autovalores_reales:
        for i, r in enumerate(autovalores_reales, 1):
            print(f"λ{i} = {r:.6g}")
    else:
        print("Ninguno.")

    if raices_extra:
        print("\nAutovalores complejos o de multiplicidad calculados de forma analítica:")
        for i, r in enumerate(raices_extra, len(autovalores_reales) + 1):
            if isinstance(r, complex):
                print(f"λ{i} = {r.real:.6g} {'+' if r.imag >= 0 else '-'} {abs(r.imag):.6g}j  (Raíz compleja)")
            else:
                print(f"λ{i} = {r:.6g} (Raíz real múltiple)")
        
    print("\nAutovectores calculados:")
    if autovectores_calculados:
        for lambd, v in autovectores_calculados:
            print(f"Para λ = {lambd:.6g} -> v = {np.array2string(v, precision=4, suppress_small=True)}")
    else:
        print("Ninguno.")
        
    print(f"\nTiempo total de ejecución: {fin - inicio:.6f} segundos.")
    input("\nPresioná Enter para volver al menú principal...")

def main():
#Menu principal de la segunda entrega de laboratorio
    while True:

        print("\n")
        print(" MENÚ PRINCIPAL ".center(40, "*"))
       # print("\n")
        print("1. Metodo de Fadeev Leverrier")
        print("2. Metodod de Trapecios")
        print("3. Salir")
        
        opcion = leer_opcion_menu("\nElegí una opción: ", ['1', '2', '3'])
        
        if opcion == "1":
            ejecutar_flujo_fadeev()
        elif opcion == "2":
            ejecutar_trapecios()
        elif opcion == "3":
            print("Fin del programa...")
            break

if __name__ == "__main__":
    main()