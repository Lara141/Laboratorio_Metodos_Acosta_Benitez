#Utilidades de entrada para el laboratorio de métodos numéricos.
#Este módulo centraliza la validación de datos ingresados por consola, como
#enteros, flotantes, opciones de menú y matrices del sistema.
import numpy as np


def leer_entero_positivo(mensaje: str) -> int:
    #Solicita y valida un entero positivo.

    #Args:
     #   mensaje: Texto mostrado al usuario antes de ingresar el valor.

    #Returns:
     #   Un entero mayor que cero.
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor > 0:
                return valor
            print("Error: Ingresá un número entero mayor que cero.")
        except ValueError:
            print("Error: Entrada inválida. Ingresá únicamente un número entero.")


def leer_float(mensaje: str) -> float:
    #Lee un número real desde la entrada estándar
    #Acepta tanto punto como coma como separador decimal
    while True:
        try:
            entrada = input(mensaje).strip().replace(",", ".")
            return float(entrada)
        except ValueError:
            print("Error: Entrada inválida. Ingresá únicamente números válidos.")


def leer_opcion_sn(mensaje: str) -> str:
    #Solicita una respuesta de tipo sí/no (s/n).
    #Returns:
     #   La respuesta en minúsculas: 's' o 'n'.
    while True:
        entrada = input(mensaje).strip().lower()
        if entrada in ['s', 'n']:
            return entrada
        print("Error: Respuesta no válida. Ingresá únicamente 's' (sí) o 'n' (no).")


def leer_opcion_menu(mensaje: str, opciones_validas: list) -> str:
    #Valida una opción elegida desde un menú interactivo.
    #Args:
     #   mensaje: Texto de la pregunta del menú.
      #  opciones_validas: Lista de respuestas permitidas.
    #Returns:
     #   La opción elegida por el usuario.
    
    while True:
        entrada = input(mensaje).strip()
        if entrada in opciones_validas:
            return entrada
        print(f"Error: Opción inválida. Elegí una de las opciones permitidas: {', '.join(opciones_validas)}.")


def ingresar_sistema() -> np.ndarray:
    #Pide al usuario una matriz cuadrada y la devuelve como array NumPy.
    #Se usa para cargar un sistema lineal para aplicar el algoritmo de Fadeev LeVerrier.
    
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

        opcion = leer_opcion_menu("\n¿Qué deseas hacer?\n1. Aplicar Fadeev Leverrier\n2. Volver a ingresar el sistema\nElegí una opción (1/2): ", ['1', '2'])
        if opcion == '1':
            return A
        elif opcion == '2':
            print("\nReiniciando la carga del sistema...")