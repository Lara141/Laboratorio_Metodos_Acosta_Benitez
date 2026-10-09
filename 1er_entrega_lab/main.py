import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import time  

from tanteo import tabla_tanteo
from interpolacion_lineal import ejecutar_interpolacion_lineal
from newton_raphson import ejecutar_newton_raphson

def main():
    while True:
       
        print(" INGRESO DE LA FUNCION") 
        print("="*50)
        str_func = input("Ingresa la función f(x) (ej. (2/3)*pi*x**3+30*pi*x**2-15000): ")

        x = sp.Symbol('x')
        try:
            expr = sp.sympify(str_func)
            f = sp.lambdify(x, expr, 'numpy')
        except Exception:
            print("Error al interpretar la función. Asegúrate de usar una sintaxis matemática válida.")
            continue  

        # Solicitamos el rango de evaluación antes de graficar y tantear
        print("\nCONFIGURACIÓN DEL RANGO DE BÚSQUEDA Y GRÁFICO")
        while True:
            try:
                inicio = float(input("Ingresa el límite inferior de x (ej. -50): "))
                fin = float(input("Ingresa el límite superior de x (ej. 20): "))
                paso = float(input("Ingresa el tamaño del paso para el tanteo (ej. 5): "))
                break
            except ValueError:
                print("Debes ingresar valores numéricos válidos. Intenta de nuevo.")

        # 1. Generar gráfico adaptativo
        print("\nGenerando gráfico...")
        plt.close('all')  
        
        # El gráfico ahora se ajusta dinámicamente a los valores ingresados por el usuario
        x_vals = np.linspace(inicio, fin, 400) 
        y_vals = f(x_vals)

        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, color='#87CEEB', linewidth=2.5, label=f'f(x) = {str_func}')
        plt.axhline(0, color='black', linewidth=1) 
        plt.axvline(0, color='black', linewidth=1) 
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        plt.title('Gráfica de la Función')
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.legend()
        
        plt.show(block=False)
        plt.pause(0.1)

        # 1.5 Aplicar Regla de los Signos de Descartes
        try:
            poly_pos = sp.Poly(expr, x)
            coeffs_pos = [c for c in poly_pos.coeffs() if c != 0] 
            
            raices_pos = sum(1 for i in range(len(coeffs_pos)-1) if coeffs_pos[i] * coeffs_pos[i+1] < 0)
            
            expr_neg = expr.subs(x, -x)
            poly_neg = sp.Poly(expr_neg, x)
            coeffs_neg = [c for c in poly_neg.coeffs() if c != 0]
            
            raices_neg = sum(1 for i in range(len(coeffs_neg)-1) if coeffs_neg[i] * coeffs_neg[i+1] < 0)
            
            print("\nPor descarte la funcion tiene:")
            print(f"- {raices_pos} raiz/raíces reales positivas (o disminuido en un número entero par).")
            print(f"- {raices_neg} raiz/raíces reales negativas (o disminuido en un número entero par).")
            
        except sp.polys.polyerrors.PolynomialError:
            print("\nPor descarte la funcion tiene: Indeterminado. La regla de Descartes solo aplica a polinomios (no a funciones trigonométricas o exponenciales).")
        except Exception:
            print("\nNo se pudo aplicar la regla de los signos de Descartes a esta función.")

        # 2. Aplicar Método de Tanteo
        print("\nMETODO DE TANTEO")
        valores, intervalos = tabla_tanteo(f, inicio, fin, paso)

        print("\nTabla de Valores generada:")
        print(f"{'x':>10} | {'f(x)':>15}")
        print("-" * 30)
        for val_x, val_y in valores:
            print(f"{val_x:10.4f} | {val_y:15.6f}")

        if intervalos:
            print(f"\n¡Se encontraron {len(intervalos)} posible(s) raíz/raíces!")
            for idx, inter in enumerate(intervalos):
                print(f"Raíz {idx + 1} detectada en el intervalo: [{inter[0]}, {inter[1]}]")
        else:
            print("\nAtención: No se detectó ningún cambio de signo en este rango.")

        # 3. Pedir el error deseado
        while True:
            try:
                error_input = float(input("\nIngresa la tolerancia deseada (ej. 0.001): "))
                break
            except ValueError:
                print("Debes ingresar un valor numérico para el error.")

        # 4. Menú interactivo de métodos
        while True:
            print("\n" + "="*30)
            print(" MENÚ DE MÉTODOS")
            print("="*30)
            print("1 - Método de Interpolación Lineal")
            print("2 - Método de Newton-Raphson")
            print("3 - Ingresa una nueva función")
            print("4 - Salir")
            
            opcion = input("Elige una opción (1, 2, 3 o 4): ")

            if opcion in ['1', '2']:
                while True:
                    print("\n--- Opciones de Intervalo ---")
                    print("1 - Utilizar el intervalo con la menor de las raíces positivas")
                    print("2 - Ingresar un intervalo manual")
                    print("3 - Volver al menú principal")
                    sub_op = input("Elige una opción (1, 2 o 3): ")
                    
                    if sub_op == '1':
                        # Filtramos los intervalos para encontrar los que puedan contener raíces positivas
                        intervalos_positivos = [inter for inter in intervalos if inter[1] > 0]
                        
                        if intervalos_positivos:
                            a, b = intervalos_positivos[0]
                            print(f"\n> Utilizando el intervalo con la menor raíz positiva: [{a}, {b}]")
                            break
                        else:
                            print("\n>> Error: No se encontraron raíces positivas en el tanteo para usar esta opción. Ingresa un intervalo manual.")
                            continue
                    elif sub_op == '2':
                        try:
                            a = float(input("\nIngresa el límite inferior (a): "))
                            b = float(input("Ingresa el límite superior (b): "))
                            break
                        except ValueError:
                            print("\nX Debes ingresar valores numéricos. Intenta de nuevo.")
                            continue
                    elif sub_op == '3':
                        break
                    else:
                        print("\nX Opción no válida.")

                if sub_op == '3':
                    continue  
                
                if opcion == '1':
                    print("\nMETODO DE INTERPOLACIÓN LINEAL")
                    inicio_tiempo = time.perf_counter()
                    
                    iteraciones_il, raiz_final_il = ejecutar_interpolacion_lineal(f, a, b, error_input)
                    
                    if raiz_final_il is None:
                        print("\nNo se obtuvo una raíz válida con Interpolación Lineal.")
                        continue 
                        
                    fin_tiempo = time.perf_counter()
                    tiempo_ejec = fin_tiempo - inicio_tiempo
                   
                    print("\nTabla de detalle de iteraciones (Interpolación Lineal):")
                    print(f"{'Iter':>5} | {'Lím. Inf (a)':>12} | {'Lím. Sup (b)':>12} | {'Aprox. (xn)':>16} | {'f(xn)':>12} | {'Error Calc.':>12}")
                    print("-" * 80)
                    for it in iteraciones_il:
                        print(f"{it['iter']:5} | {it['a']:12.6f} | {it['b']:12.6f} | {it['xr']:16.6f} | {it['fxn']:12.6f} | {it['error']:12.8f}")

                    print("\n" + "="*50)
                    print(f" RESULTADO DEL METODO INTERPOLACIÓN LINEAL: El valor aproximado de la raíz es {raiz_final_il:.6f} con error menor a {error_input}.")
                    print(f" Total de iteraciones requeridas: {len(iteraciones_il)}")
                    print(f" Tiempo de ejecución: {tiempo_ejec:.6f} segundos")
               
                elif opcion == '2':
                    print("\nMETODO DE NEWTON-RAPHSON")
                    inicio_tiempo = time.perf_counter()
                    
                    iteraciones_nr, raiz_final_nr = ejecutar_newton_raphson(str_func, a, b, error_input)

                    if raiz_final_nr is None:
                        print("\nNo se obtuvo una raíz válida con Newton-Raphson.")
                        continue

                    fin_tiempo = time.perf_counter()
                    tiempo_ejec = fin_tiempo - inicio_tiempo

                    print("\nTabla de detalle de iteraciones (Newton-Raphson):")
                    print(f"{'Iter':>5} | {'Aprox. Ant (xn-1)':>18} | {'f(xn-1)':>12} | {' f(derivada) (xn-1)':>12} | {'Aprox. Nueva (xn)':>18} | {'Error Calc.':>12}")
                    print("-" * 90)
                    for it in iteraciones_nr:
                        print(f"{it['iter']:5} | {it['x_ant']:18.6f} | {it['fx']:12.6f} | {it['dfx']:12.6f} | {it['x_act']:18.6f} | {it['error']:12.8f}")

                    print("\n" + "="*50)
                    print(f" RESULTADO DEL METODO NEWTON-RAPHSON: El valor aproximado de la raíz es {raiz_final_nr:.6f} con un error menor a {error_input}.")
                    print(f" Total de iteraciones requeridas: {len(iteraciones_nr)}")
                    print(f" Tiempo de ejecución: {tiempo_ejec:.6f} segundos")
                 
            elif opcion == '3':
                print("\nReiniciando programa para ingresar una nueva función...\n")
                break  
            
            elif opcion == '4':
                print("\nSaliendo del programa...")
                return  
            
            else:
                print("\nOpción no válida, por favor ingresa 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()