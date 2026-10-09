import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import time  
from tanteo import tabla_tanteo
from intervalo_medio import calcular_iteraciones_teoricas, ejecutar_intervalo_medio
from interpolacion_lineal import ejecutar_interpolacion_lineal

def main():
    print("INGRESO DE LA FUNCION")
    str_func = input("Ingresa la función f(x) (ej. x**2 - 4 o exp(-x) - x): ")

    # Configuramos sympy para interpretar el texto matemático ingresado
    x = sp.Symbol('x')
    try:
        expr = sp.sympify(str_func)
        # Convertimos la expresión simbólica en una función ejecutable por numpy
        f = sp.lambdify(x, expr, 'numpy')
    except Exception:
        print("Error al interpretar la función. Asegúrate de usar una sintaxis matemática válida.")
        return

    # 1. Mostrar el gráfico de la función ingresada (Gráfico no bloqueante)
    print("\nGenerando gráfico...")
    x_vals = np.linspace(0, 300, 400)
    y_vals = f(x_vals)

    plt.figure(figsize=(8, 6))
    # Usamos un tono celeste pastel para el trazo de la gráfica principal
    plt.plot(x_vals, y_vals, color='#87CEEB', linewidth=2.5, label=f'f(x) = {str_func}')
    plt.axhline(0, color='black', linewidth=1) # Eje X
    plt.axvline(0, color='black', linewidth=1) # Eje Y
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.title('Gráfica de la Función')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.legend()
    
    # Se muestra el gráfico sin detener la ejecución del código
    plt.show(block=False)
    plt.pause(0.1)

    # 2. Aplicar Método de Tanteo
    print("\nMETODO DE TANTEO")
    try:
        inicio = float(input("Ingresa el valor inicial del intervalo de búsqueda (ej. -5): "))
        fin = float(input("Ingresa el valor final del intervalo de búsqueda (ej. 5): "))
        paso = float(input("Ingresa el tamaño del paso de incremento (ej. 0.5): "))
    except ValueError:
        print("Debes ingresar valores numéricos válidos.")
        return

    # Ahora desempaquetamos intervalos como una lista
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
            
        a, b = intervalos[0]
        print(f"\n>> Se utilizará automáticamente el intervalo de la menor raíz para los métodos: [{a}, {b}]")
    else:
        print("\nNo se detectó ningún cambio de signo en este rango, vuelve a intentarlo con otros valores")
        return

    # 3. Pedir el error deseado antes del menú
    try:
        error_input = float(input("\nIngresa la cota de error (tolerancia) deseada (ej. 0.001): "))
    except ValueError:
        print("Debes ingresar un valor numérico para el error.")
        return

    # 4. Menú interactivo
    while True:
      
        print("\n MENÚ DE MÉTODOS")
        print("1 - Método del Intervalo Medio")
        print("2 - Método de Interpolación Lineal")
        print("3 - Salir")
        
        opcion = input("Elige una opción (1, 2 o 3): ")

        if opcion == '1':
            print("\nMETODO DEL INTERVALO MEDIO")
            iter_teoricas = calcular_iteraciones_teoricas(a, b, error_input)
            print(f"\n>> Cantidad de iteraciones teóricas calculadas para este error: {iter_teoricas} iteraciones.")

            # Iniciar el temporizador
            inicio_tiempo = time.perf_counter()
            
            iteraciones, raiz_final = ejecutar_intervalo_medio(f, a, b, error_input)

            # Detener el temporizador
            fin_tiempo = time.perf_counter()
            tiempo_ejec = fin_tiempo - inicio_tiempo

            print("\nDetalle paso a paso del Método de Bisección:")
            print(f"{'Iter':>5} | {'Lím. Inf (a)':>12} | {'Lím. Sup (b)':>12} | {'Punto Medio (xr)':>18} | {'Error Calc.':>12}")
            print("-" * 70)
            for it in iteraciones:
                print(f"{it['iter']:5} | {it['a']:12.6f} | {it['b']:12.6f} | {it['xr']:18.6f} | {it['error']:12.6f}")

            print("\n" + "="*50)
            print(f" RESULTADO DEL INTERVALO MEDIO: El valor aproximado de la raíz es {raiz_final:.6f}")
            print(f" Total de iteraciones requeridas: {len(iteraciones)}")
            print(f" Tiempo de ejecución: {tiempo_ejec:.6f} segundos")
            print("-"*50)

        elif opcion == '2':
            print("\nMETODO DE INTERPOLACIÓN LINEAL")
            
            # Iniciar el temporizador
            inicio_tiempo = time.perf_counter()
            
            iteraciones_il, raiz_final_il = ejecutar_interpolacion_lineal(f, a, b, error_input)

            # Detener el temporizador
            fin_tiempo = time.perf_counter()
            tiempo_ejec = fin_tiempo - inicio_tiempo

            print("\nDetalle paso a paso del Método de Interpolación Lineal:")
            print(f"{'Iter':>5} | {'Lím. Inf (a)':>12} | {'Lím. Sup (b)':>12} | {'Aprox. (xr)':>18} | {'Error Calc.':>12}")
            print("-" * 70)
            for it in iteraciones_il:
                print(f"{it['iter']:5} | {it['a']:12.6f} | {it['b']:12.6f} | {it['xr']:18.6f} | {it['error']:12.6f}")

            print("\n" + "="*50)
            print(f" RESULTADO INTERPOLACIÓN: El valor aproximado es {raiz_final_il:.6f}")
            print(f" Total de iteraciones requeridas: {len(iteraciones_il)}")
            print(f" Tiempo de ejecución: {tiempo_ejec:.6f} segundos")
            print("-"*50)

        elif opcion == '3':
            print("\nSaliendo del programa")
            break
        
        else:
            print("\nOpción no válida, por favor ingresa 1, 2 o 3.")

if __name__ == "__main__":
    main()
