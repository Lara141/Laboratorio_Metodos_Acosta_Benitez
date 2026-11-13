import numpy as np
from entrada import leer_entero_positivo, leer_float, leer_opcion_menu

def ejecutar_trapecios():
   
    print("MÉTODO DE LOS TRAPECIOS")
    print("-"*50)
    
    # 1. Ingreso y validación
    while True:
        n_pares = leer_entero_positivo("Ingresá la cantidad total de pares de datos (x, y): ")
        if n_pares >= 2:
            break
        print("Error: Se necesitan al menos 2 pares de datos para formar un trapecio.")
        
    x_vals = []
    y_vals = []
    
    print("\nIngresá los valores numéricos para cada par.")
    for i in range(n_pares):
        while True:
            print(f"\nPar {i+1}:")
            x = leer_float("x: ")
            if i > 0 and x <= x_vals[-1]:
                print(f"Error: El valor de x debe ser estrictamente mayor que el anterior ({x_vals[-1]:g}). Volvé a ingresar el par completo.")
                continue
            y = leer_float("y: ")
            x_vals.append(x)
            y_vals.append(y)
            break
            
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    
    # 2. Análisis de diferencias y visualización de tramos
    print("\nAnálisis de diferencias (h) entre puntos consecutivos")
    h_diffs = np.diff(x_vals)
    for i in range(len(h_diffs)):
        print(f"Tramo {i+1} [x = {x_vals[i]:g} a x = {x_vals[i+1]:g}]: h = {h_diffs[i]:g}")
        
    # Agrupación por intervalos con el mismo h
    intervalos = []
    tol = 1e-9
    start_idx = 0
    current_h = h_diffs[0]
    
    for i in range(1, len(h_diffs)):
        if abs(h_diffs[i] - current_h) > tol:
            intervalos.append({
                "x": x_vals[start_idx:i+1],
                "y": y_vals[start_idx:i+1],
                "h": current_h
            })
            start_idx = i
            current_h = h_diffs[i]
            
    # Cerrar el último grupo
    intervalos.append({
        "x": x_vals[start_idx:len(h_diffs)+1],
        "y": y_vals[start_idx:len(h_diffs)+1],
        "h": current_h
    })
    
    print("\nIntervalos de integración identificados")
    for i, inter in enumerate(intervalos, 1):
        n_sub = len(inter['x']) - 1
        print(f"Intervalo {i}: Desde x = {inter['x'][0]:g} hasta x = {inter['x'][-1]:g} | h = {inter['h']:g} | Subintervalos: {n_sub}")
        
    opcion = leer_opcion_menu("\n¿Qué querés hacer?\n1. Aplicar a todos los intervalos\n2. Aplicar solo a un intervalo\nElegí una opción (1/2): ", ['1', '2'])
    
    intervalos_a_calcular = []
    indices_calc = []
    
    if opcion == '1':
        intervalos_a_calcular = intervalos
        indices_calc = list(range(1, len(intervalos) + 1))
    else:
        while True:
            idx = leer_entero_positivo(f"Ingresá el número de intervalo a calcular (1 a {len(intervalos)}): ")
            if 1 <= idx <= len(intervalos):
                intervalos_a_calcular = [intervalos[idx-1]]
                indices_calc = [idx]
                break
            print(f"Error: Intervalo inválido. Debe ser un número entre 1 y {len(intervalos)}.")
            
    # 3. Cálculo de cada intervalo
    resultados = []
    suma_total = 0.0
    
    for num_int, inter in zip(indices_calc, intervalos_a_calcular):
        print(f"Cálculo del Intervalo {num_int}")
        print("."*50)
        
        x = inter['x']
        y = inter['y']
        h = inter['h']
        n = len(x) - 1
        
        print(f"Punto inicial: (x = {x[0]:g}, y = {y[0]:g})")
        print(f"Punto final:   (x = {x[-1]:g}, y = {y[-1]:g})")
        print(f"Valor de h: {h:g}")
        print(f"Cantidad de subintervalos (n): {n}")
        
        if n == 1:
            print("\nFórmula utilizada: Trapecio simple")
            print("T ≈ (h / 2) * (y_0 + y_1)")
            
            y0, y1 = y[0], y[1]
            print(f"\nSustitución:")
            print(f"T ≈ ({h:g} / 2) * ({y0:g} + {y1:g})")
            
            T = (h / 2) * (y0 + y1)
            print(f"T ≈ {T:g}")
        else:
            print("\nFórmula utilizada: Regla de trapecios compuesta")
            print("T ≈ (h / 2) * (E + 2P + 2I)")
            
            E = y[0] + y[-1]
            print(f"\nE (Suma de extremos) = y_0 + y_n")
            print(f"E = {y[0]:g} + {y[-1]:g} = {E:g}")
            
            valores_P = [y[i] for i in range(2, len(y)-1, 2)]
            valores_I = [y[i] for i in range(1, len(y)-1, 2)]
            
            P_sum = sum(valores_P)
            I_sum = sum(valores_I)
            
            print(f"\nP (Suma de interiores con índice par):")
            if valores_P:
                text_P = " + ".join(f"{v:g}" for v in valores_P)
                print(f"P = {text_P} = {P_sum:g}")
            else:
                print("P = 0 (No hay valores)")
                
            print(f"\nI (Suma de interiores con índice impar):")
            if valores_I:
                text_I = " + ".join(f"{v:g}" for v in valores_I)
                print(f"I = {text_I} = {I_sum:g}")
            else:
                print("I = 0 (No hay valores)")
                
            print(f"\nSustitución en la fórmula:")
            print(f"T ≈ ({h:g} / 2) * ({E:g} + 2*({P_sum:g}) + 2*({I_sum:g}))")
            
            T = (h / 2) * (E + 2*P_sum + 2*I_sum)
            print(f"T ≈ {T:g}")
            
        resultados.append({
            "num": num_int,
            "x_ini": x[0],
            "x_fin": x[-1],
            "h": h,
            "n": n,
            "T": T
        })
        suma_total += T
        
    # 4. Resultados finales
    print("\n" + "-"*50)
    print("RESULTADOS FINALES DE LA INTEGRACIÓN")
    print("-"*50)
    print(f"{'Int.':<5} | {'x_ini':<10} | {'x_fin':<10} | {'h':<10} | {'n sub.':<8} | {'Resultado (T)':<15}")
    print("-" * 65)
    for r in resultados:
        print(f"{r['num']:<5} | {r['x_ini']:<10.4g} | {r['x_fin']:<10.4g} | {r['h']:<10.4g} | {r['n']:<8} | {r['T']:<15.6g}")
    print("-" * 65)
    
    print("\nResultado final:")
    if len(resultados) == 1:
        # Solo se calculó un intervalo
        num_unico = resultados[0]['num']
        print(f"T_{num_unico} = {suma_total:g}")
    else:
        # Se calcularon múltiples intervalos
        terminos_variables = " + ".join([f"T_{r['num']}" for r in resultados])
        terminos_numericos = " + ".join([f"{r['T']:g}" for r in resultados])
        
        print(f"T_total = {terminos_variables}")
        print(f"T_total = {terminos_numericos}")
        print(f"T_total = {suma_total:g}")
        
    input("\nPresioná Enter para volver al menú principal...")