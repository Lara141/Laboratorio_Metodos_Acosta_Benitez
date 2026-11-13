import numpy as np

def leer_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor > 0:
                return valor
            print("Error: Ingresá un número entero mayor que cero.")
        except ValueError:
            print("Error: Entrada inválida. Ingresá únicamente un número entero.")

def leer_float(mensaje: str) -> float:
    while True:
        try:
            entrada = input(mensaje).strip().replace(",", ".")
            return float(entrada)
        except ValueError:
            print("Error: Entrada inválida. Ingresá únicamente números válidos.")

def leer_opcion_sn(mensaje: str) -> str:
    while True:
        entrada = input(mensaje).strip().lower()
        if entrada in ['s', 'n']:
            return entrada
        print("Error: Respuesta no válida. Ingresá únicamente 's' (sí) o 'n' (no).")

def leer_opcion_menu(mensaje: str, opciones_validas: list) -> str:
    while True:
        entrada = input(mensaje).strip()
        if entrada in opciones_validas:
            return entrada
        print(f"Error: Opción inválida. Elegí una de las opciones permitidas: {', '.join(opciones_validas)}.")

def ingresar_sistema() -> np.ndarray:
    print("\n--- Ingreso de la Matriz del Sistema ---")
    print("El sistema debe ser cuadrado (misma cantidad de ecuaciones e incógnitas).")
    n = leer_entero_positivo("Ingresá el orden de la matriz (N): ")
    
    while True:
        print(f"\nIngresá los coeficientes fila por fila.")
        print(f"Para cada fila, escribí {n} números separados por espacios (usá punto o coma para decimales).")
        
        filas = []
        for i in range(n):
            while True:
                entrada = input(f"Fila {i + 1}: ").strip()
                if not entrada:
                    print("Error: No podés dejar la fila vacía. Volvé a ingresarla.")
                    continue
                
                try:
                    valores = [float(v.replace(",", ".")) for v in entrada.split()]
                    if len(valores) != n:
                        print(f"Error: Se esperaban {n} valores, pero ingresaste {len(valores)}. Volvé a ingresar la fila.")
                        continue
                    filas.append(valores)
                    break
                except ValueError:
                    print("Error: Entrada inválida. Asegurate de ingresar solo números separados por espacios.")
                    
        A = np.array(filas, dtype=float)
        
        print("\nMatriz ingresada:")
        print(A)
        
        opcion = leer_opcion_menu("\n¿Qué querés hacer?\n1. Aplicar Faddeev-Leverrier\n2. Volver a ingresar el sistema\nElegí una opción (1/2): ", ['1', '2'])
        if opcion == '1':
            return A
        elif opcion == '2':
            print("\nReiniciando la carga del sistema...")