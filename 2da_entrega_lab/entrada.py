import numpy as np

def leer_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("Error: Ingresá un número entero mayor que cero.")
        except ValueError:
            print("Entrada inválida: ingresá un número entero.")

def ingresar_sistema() -> np.ndarray:
    print("\n--- Ingreso de la Matriz del Sistema ---")
    print("El sistema debe ser cuadrado (misma cantidad de ecuaciones e incógnitas).")
    n = leer_entero_positivo("Ingresá el orden de la matriz (N): ")
    
    while True:
        print(f"\nIngresá los coeficientes fila por fila.")
        print(f"Para cada fila, escribí {n} números separados por espacios (usá punto o coma para decimales).")
        
        filas = []
        error_en_carga = False
        
        for i in range(n):
            while True:
                entrada = input(f"Fila {i + 1}: ").strip()
                if not entrada:
                    print("Error: No podés dejar la fila vacía. Volvé a ingresarla.")
                    continue
                
                try:
                    # Se reemplaza coma por punto y se convierte a float sin usar eval()
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
        
        opcion = input("\n¿Qué querés hacer?\n1. Aplicar Faddeev-Leverrier\n2. Volver a ingresar el sistema\nElegí una opción (1/2): ").strip()
        if opcion == '1':
            return A
        elif opcion == '2':
            print("\nReiniciando la carga del sistema...")
        else:
            print("\nOpción no reconocida. Asumiendo que se desea continuar con Faddeev-Leverrier.")
            return A