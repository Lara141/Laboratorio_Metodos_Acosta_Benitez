
# ==========================================================
# LABORATORIO 6 - METODO DE TRAPECIOS
# PROGRAMA PRINCIPAL
# ==========================================================

from trapecios import metodo_trapecios, generar_datos_funcion


def ingresar_datos_tabulados():
    """
    Solicita los valores X e Y de una tabla.
    """

    print("\n--- INGRESO DE DATOS TABULADOS ---")

    n = int(input("Ingrese la cantidad de puntos: "))

    if n < 2:
        raise ValueError("Se necesitan al menos dos puntos.")

    x = []
    y = []

    for i in range(n):
        print(f"\nPunto {i}:")
        xi = float(input(f"  X{i}: "))
        yi = float(input(f"  Y{i}: "))

        x.append(xi)
        y.append(yi)

    return x, y


def ingresar_funcion():
    """
    Solicita una funcion, los limites de integracion
    y la cantidad de subintervalos.
    """

    print("\n--- INGRESO DE FUNCION MATEMATICA ---")

    expresion = input("Ingrese f(x): ")

    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))
    n = int(input("Cantidad de subintervalos: "))

    x, y = generar_datos_funcion(expresion, a, b, n)

    return x, y, (expresion, a, b)


def mostrar_tabla(x, y):
    """
    Muestra los puntos utilizados en la integracion.
    """

    print("\n--- TABLA DE VALORES ---")
    print(f"{'i':<8}{'X':<15}{'Y':<15}")
    print("-" * 38)

    for i in range(len(x)):
        print(f"{i:<8}{x[i]:<15.6f}{y[i]:<15.6f}")


def mostrar_resultados(x, y):
    """
    Ejecuta el metodo de Trapecios y presenta
    el procedimiento y el resultado final.
    """

    resultado = metodo_trapecios(x, y)

    mostrar_tabla(x, y)

    h = resultado["h"]
    n = resultado["n"]
    E = resultado["E"]
    P = resultado["P"]
    I = resultado["I"]
    A = resultado["resultado"]

    print("\n--- PROCEDIMIENTO ---")

    print(f"\nCantidad de subintervalos: n = {n}")
    print(f"Amplitud: h = {h:.6f}")

    print("\nSumatorias:")
    print(f"E = {E:.6f}")
    print(f"P = {P:.6f}")
    print(f"I = {I:.6f}")

    print("\nFormula de Trapecios:")
    print("A = (h / 2) * (E + 2P + 2I)")

    print("\nSustitucion:")
    print(
        f"A = ({h:.6f} / 2) * "
        f"({E:.6f} + 2({P:.6f}) + 2({I:.6f}))"
    )

    print("\n--- RESULTADO FINAL ---")
    print(f"A = {A:.8f}")


def mostrar_menu():
    """
    Muestra las opciones disponibles.
    """

    print("\n" + "=" * 55)
    print("          METODO DE TRAPECIOS")
    print("=" * 55)

    print("1. Integrar mediante datos tabulados")
    print("2. Integrar mediante una funcion matematica")
    print("3. Calcular nuevamente con datos anteriores")
    print("4. Salir")


def main():
    """
    Controla el menu principal y la ejecucion
    del programa.
    """

    datos_anteriores = None
    funcion_anterior = None

    while True:

        mostrar_menu()

        opcion = input("\nSeleccione una opcion: ")

        try:

            if opcion == "1":

                x, y = ingresar_datos_tabulados()

                mostrar_resultados(x, y)

                datos_anteriores = (x, y)
                funcion_anterior = None

            elif opcion == "2":

                x, y, datos_funcion = ingresar_funcion()

                mostrar_resultados(x, y)

                datos_anteriores = (x, y)
                funcion_anterior = datos_funcion

            elif opcion == "3":

                if datos_anteriores is None:
                    print("\nNo hay datos anteriores.")
                    continue

                if funcion_anterior is not None:

                    expresion, a, b = funcion_anterior

                    print("\nFuncion anterior:", expresion)
                    print(f"Intervalo: [{a}, {b}]")

                    respuesta = input(
                        "Desea cambiar la cantidad de "
                        "subintervalos? (s/n): "
                    ).lower()

                    if respuesta == "s":

                        n = int(input(
                            "Nueva cantidad de subintervalos: "
                        ))

                        x, y = generar_datos_funcion(
                            expresion, a, b, n
                        )

                        mostrar_resultados(x, y)
                        datos_anteriores = (x, y)

                    else:
                        x, y = datos_anteriores
                        mostrar_resultados(x, y)

                else:
                    x, y = datos_anteriores
                    mostrar_resultados(x, y)

            elif opcion == "4":

                print("\nFinalizando el programa...")
                print("Gracias por utilizar el metodo de Trapecios.")
                break

            else:
                print("\nOpcion no valida. Intente nuevamente.")

        except (ValueError, TypeError, ZeroDivisionError,
                OverflowError) as error:
            print(f"\nERROR: {error}")

        except Exception as error:
            print(f"\nNo se pudo realizar el calculo: {error}")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
