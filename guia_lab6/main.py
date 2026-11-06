
# ==========================================================
# METODO DE INTEGRACION NUMERICA: TRAPECIOS
# ==========================================================

def verificar_equidistancia(x, tolerancia=1e-9):
    """
    Verifica que todos los subintervalos tengan
    la misma amplitud.

    Retorna la amplitud h si son equidistantes.
    """

    if len(x) < 2:
        raise ValueError("Se necesitan al menos dos puntos.")

    # Calculamos la amplitud del primer subintervalo
    h = x[1] - x[0]

    if h <= 0:
        raise ValueError("Los valores de X deben ser crecientes.")

    # Comparamos las amplitudes de los subintervalos
    for i in range(1, len(x) - 1):
        diferencia = x[i + 1] - x[i]

        if abs(diferencia - h) > tolerancia * max(1, abs(h)):
            raise ValueError(
                "Los subintervalos no son equidistantes."
            )

    return h


def calcular_sumatorias(y):
    """
    Calcula los valores E, P e I de la formula
    de Trapecios.
    """

    # Suma de los extremos
    E = y[0] + y[-1]

    # Suma de las posiciones interiores pares
    P = sum(y[i] for i in range(2, len(y) - 1, 2))

    # Suma de las posiciones interiores impares
    I = sum(y[i] for i in range(1, len(y) - 1, 2))

    return E, P, I


def metodo_trapecios(x, y):
    """
    Aplica el metodo compuesto de Trapecios
    utilizando la formula de la catedra:

    A = (h / 2) * (E + 2P + 2I)
    """

    # Verificamos que ambas listas tengan igual longitud
    if len(x) != len(y):
        raise ValueError(
            "La cantidad de valores X e Y debe coincidir."
        )

    # Verificamos equidistancia y obtenemos h
    h = verificar_equidistancia(x)

    # Calculamos las sumatorias
    E, P, I = calcular_sumatorias(y)

    # Aplicamos la formula de Trapecios
    A = (h / 2) * (E + 2 * P + 2 * I)

    # Cantidad de subintervalos
    n = len(x) - 1

    # Devolvemos los resultados al archivo main
    return {
        "h": h,
        "n": n,
        "E": E,
        "P": P,
        "I": I,
        "resultado": A
    }
