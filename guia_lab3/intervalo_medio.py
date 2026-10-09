import math

def calcular_iteraciones_teoricas(a, b, error_deseado):
    """
    Calcula cuántas iteraciones (n) son necesarias teóricamente para que 
    el error no supere el error deseado (E).
    Fórmula utilizada: n >= (ln(b - a) - ln(E)) / ln(2)
    """
    # Aplicamos la fórmula logarítmica para despejar la cantidad de iteraciones[cite: 3]
    n = (math.log(b - a) - math.log(error_deseado)) / math.log(2)
    return math.ceil(n)

def ejecutar_intervalo_medio(f, a, b, error_deseado):
    """
    Aplica el método de bisección dividiendo siempre el intervalo a la mitad.
    Devuelve una lista con el historial de cada iteración y el valor final de la raíz.
    """
    iteraciones = []
    n = 1 
    
    while True:
        # La posición de la raíz se aproxima situándola en el punto medio del subintervalo[cite: 3, 4]
        xr = (a + b) / 2.0
        
        # El error en el método de bisección está acotado por la mitad del intervalo actual
        error_calculado = (b - a) / 2.0

        # Guardamos los datos de la iteración actual para mostrarlos en la tabla
        iteraciones.append({
            'iter': n,
            'a': a,
            'b': b,
            'xr': xr,
            'error': error_calculado
        })

        # Criterio de parada: si el error calculado es menor al error ingresado, terminamos
        if error_calculado < error_deseado:
            break

        # Evaluamos en qué subintervalo quedó encerrada la raíz[cite: 3, 4]
        if f(a) * f(xr) < 0:
            b = xr  # La raíz está en el subintervalo izquierdo
        elif f(a) * f(xr) > 0:
            a = xr  # La raíz está en el subintervalo derecho
        else:
            break   # La función evaluada en xr es 0, encontramos la raíz exacta

        n += 1

    return iteraciones, xr