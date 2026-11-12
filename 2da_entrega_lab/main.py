import time
import numpy as np
from entrada import ingresar_sistema
from fadeev_leverrier import calcular_faddeev, calcular_autovector
from descartes import analisis_descartes
from biseccion import evaluar_polinomio, ejecutar_biseccion
from trapecios import ejecutar_trapecios

def busqueda_autovalores(coeficientes):
    analisis_descartes(coeficientes)
    
    raices_encontradas = []
    
    while True:
        resp = input("\n¿Querés tantear raíces en un intervalo? (s/n): ").strip().lower()
        if resp != 's':
            break
            
        try:
            inicio = float(input("Valor inicial del tanteo: ").replace(",", "."))
            fin = float(input("Valor final del tanteo: ").replace(",", "."))
            paso = float(input("Incremento: ").replace(",", "."))
            
            if inicio >= fin or paso <= 0:
                print("Intervalo o incremento inválido.")
                continue
                
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
                
                # Raíz exacta detectada
                if abs(y) < 1e-10:
                    print(f"*** Raíz exacta encontrada en λ = {x} ***")
                    if not any(abs(x - r) < 1e-3 for r in raices_encontradas):
                        raices_encontradas.append(x)
                        
                # Cambio de signo
                if prev_y is not None and abs(y) >= 1e-10 and np.sign(y) != np.sign(prev_y):
                    intervalos_cambio.append((prev_x, x))
                    
                prev_x = x
                prev_y = y
                
            if intervalos_cambio:
                print("\nSe detectaron cambios de signo en los siguientes intervalos:")
                for a, b in intervalos_cambio:
                    print(f"[{a:.4g}, {b:.4g}]")
                    
                for a, b in intervalos_cambio:
                    acc = input(f"\nPara el intervalo [{a:.4g}, {b:.4g}], ¿querés aplicar bisección? (s/n): ").strip().lower()
                    if acc == 's':
                        raiz = ejecutar_biseccion(coeficientes)
                        if raiz is not None:
                            # Evitar duplicados
                            if not any(abs(raiz - r) < 1e-3 for r in raices_encontradas):
                                raices_encontradas.append(raiz)
                            else:
                                print("Esta raíz ya estaba en la lista de encontradas.")
                                
        except ValueError:
            print("Por favor, ingresá valores numéricos válidos.")
            
    return raices_encontradas

def ejecutar_flujo_faddeev():
    A = ingresar_sistema()
    inicio = time.perf_counter()
    
    # 1. Faddeev-Leverrier
    b_k_list, coeficientes, polinomio_str = calcular_faddeev(A)
    
    # 2. Búsqueda de autovalores
    autovalores_reales = []
    if input("\n¿Querés buscar los autovalores? (s/n): ").strip().lower() == 's':
        autovalores_reales = busqueda_autovalores(coeficientes)
        
    # 3. Autovectores
    autovectores_calculados = []
    if autovalores_reales:
        print("\nAutovalores reales encontrados:", [round(r, 6) for r in autovalores_reales])
        print("\n¿Qué deseas hacer con los autovectores?")
        print("1. Buscar los autovectores de TODOS los autovalores encontrados")
        print("2. Buscar UN SOLO autovector")
        print("3. Volver al menú principal")
        
        opc_vec = input("Elegí una opción: ").strip()
        if opc_vec == '1':
            for lambd in autovalores_reales:
                v = calcular_autovector(A, lambd)
                autovectores_calculados.append((lambd, v))
        elif opc_vec == '2':
            try:
                val = float(input("Ingresá el autovalor para calcular su autovector: ").replace(",", "."))
                # Verificar si está en la lista (con tolerancia)
                match = [r for r in autovalores_reales if abs(r - val) < 1e-3]
                if match:
                    lambd_real = match[0]
                    print(f"Autovalor aceptado (aproximado a {lambd_real}).")
                    v = calcular_autovector(A, lambd_real)
                    autovectores_calculados.append((lambd_real, v))
                else:
                    print("El valor ingresado no coincide con ninguna de las raíces reales encontradas en este análisis.")
            except ValueError:
                print("Valor inválido.")
    
    fin = time.perf_counter()
    
    # 4. Resumen final
    print("\n" + "="*50)
    print("RESUMEN FINAL DE FADDEEV-LEVERRIER")
    print("="*50)
    print("Valores b_k calculados:")
    for i, b in enumerate(b_k_list, 1):
        print(f"b_{i} = {b:g}")
        
    print(f"\nPolinomio característico:\np(λ) = {polinomio_str} = 0")
    
    print("\nAutovalores reales encontrados:")
    if autovalores_reales:
        for r in autovalores_reales:
            print(f"λ = {r:.6g}")
    else:
        print("No se calcularon/encontraron autovalores reales en esta sesión.")
        
    print("\nAclaración: Descartes, tanteo y bisección buscan únicamente raíces reales. Si el polinomio tiene raíces complejas, se requeriría un método numérico adicional (como Bairstow) para calcularlas.")
    
    print("\nAutovectores calculados:")
    if autovectores_calculados:
        for lambd, v in autovectores_calculados:
            print(f"Para λ = {lambd:.6g} -> v = {np.array2string(v, precision=4)}")
    else:
        print("Ninguno.")
        
    print(f"\nTiempo total de ejecución: {fin - inicio:.6f} segundos.")
    input("\nPresioná Enter para volver al menú principal...")

def main():
    while True:
        print("\n" + "*"*40)
        print(" MENÚ PRINCIPAL ".center(40, "*"))
        print("*"*40)
        print("1. Resolver un problema con Faddeev-Leverrier")
        print("2. Resolver un problema con trapecios")
        print("3. Salir")
        
        opcion = input("\nElegí una opción: ").strip()
        if opcion == "1":
            ejecutar_flujo_faddeev()
        elif opcion == "2":
            ejecutar_trapecios()
        elif opcion == "3":
            print("Fin del programa. ¡Éxitos con el proyecto!")
            break
        else:
            print("Opción inválida. Elegí 1, 2 o 3.")

if __name__ == "__main__":
    main()