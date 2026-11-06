
# ==========================================================
# LABORATORIO 6 - METODO DE TRAPECIOS
# PROGRAMA PRINCIPAL
# ==========================================================

from trapecios import metodo_trapecios


def ingresar_datos():
    """
    Solicita los valores X e Y de la tabla.
    """

    print("\n--- INGRESO DE DATOS ---")

    cantidad = int(input("Ingrese la cantidad de puntos: "))

    if cantidad < 2:
        raise ValueError("Se necesitan al menos dos puntos.")

    x = []
    y = []

    for i in range(cantidad):
        print(f"\nPunto {i}:")
        xi = float(input(f"  X{i}: "))
        yi = float(input(f"  Y{i}: "))

        x.append(xi)
        y.append(yi)

    return x, y


def mostrar_tabla(x, y):
    """
    Muestra los valores utilizados en el calculo.
    """

    print("\n--- TABLA DE VALORES ---")
    print(f"{'i':<8}{'X':<15}{'Y':<15}")
    print("-" * 38)

    for i in range(len(x)):
        print(f"{i:<8}{x[i]:<15.6f}{y[i]:<15.6f}")


def mostrar_sumatoria(nombre, valores, resultado):
    """
    Muestra los terminos que forman una sumatoria
    y su resultado.
    """

    if not valores:
        print(f"{nombre} = 0 (sin valores interiores)")
        return

    # Convertimos los valores en texto
    terminos = " + ".join(f"({v:.6f})" for v in valores)

    print(f"{nombre} = {terminos}")
    print(f"{nombre} = {resultado:.6f}")


def mostrar_resultados(x, y):
    """
    Presenta la tabla, las sumatorias,
    la sustitucion y el resultado final.
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

    print("\nCalculo de la amplitud:")
    print("h = (b - a) / n")
    print(f"h = ({x[-1]:.6f} - {x[0]:.6f}) / {n}")
    print(f"h = {h:.6f}")

    print("\n--- CALCULO DE SUMATORIAS ---")

    print("\nExtremos (E):")
    mostrar_sumatoria("E", resultado["valores_E"], E)

    print("\nPosiciones pares interiores (P):")
    mostrar_sumatoria("P", resultado["valores_P"], P)

    print("\nPosiciones impares interiores (I):")
    mostrar_sumatoria("I", resultado["valores_I"], I)

    print("\n--- APLICACION DE LA FORMULA ---")

    print("\nFormula de Trapecios:")
    print("A = (h / 2) * (E + 2P + 2I)")

    print("\nSustitucion:")
    print(
        f"A = ({h:.6f} / 2) * "
        f"({E:.6f} + 2({P:.6f}) + 2({I:.6f}))"
    )

    suma = E + 2 * P + 2 * I

    print("\nOperaciones:")
    print(f"A = ({h:.6f} / 2) * ({suma:.6f})")

    print("\n" + "=" * 55)
    print(f"RESULTADO FINAL: A = {A:.8f}")
    print("=" * 55)


def mostrar_menu():
    """
    Muestra las opciones disponibles.
    """

    print("\n" + "=" * 55)
    print("                  METODO DE TRAPECIOS")
    print("=" * 55)

    print("1. Ingresar valores de X e Y")
    print("2. Salir")


def main():
    """
    Controla el menu y permite reutilizar
    los datos ingresados anteriormente.
    """

    datos_anteriores = None

    while True:

        mostrar_menu()

        opcion = input("\nSeleccione una opcion: ")

        try:

            if opcion == "1":

                x, y = ingresar_datos()

                mostrar_resultados(x, y)

                datos_anteriores = (x, y)

            elif opcion == "2":

                print("\nFinalizando el programa...")
                break

            else:
                print("\nOpcion no valida. Intente nuevamente.")

        except (ValueError, TypeError, OverflowError) as error:
            print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
