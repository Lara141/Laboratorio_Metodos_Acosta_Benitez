
def ejecutar_interpolacion_lineal(f, a, b, error_deseado):
    iteraciones = []
    n = 1
    xr_anterior = None
    
    while True:
        # Evaluamos la función en los extremos
        fa = f(a)
        fb = f(b)
        
        # Evitar división por cero si f(a) y f(b) son iguales
        if fa - fb == 0:
            print("Error: f(a) y f(b) son iguales, división por cero.")
            break
            
        # Fórmula de Interpolación Lineal
        xr = b - (fb * (a - b)) / (fa - fb)
        
        # Calcular el error estimado (diferencia entre aproximaciones sucesivas)
        if xr_anterior is not None:
            error_calculado = abs(xr - xr_anterior)
        else:
            error_calculado = abs(b - a) # Error referencial para la iteración 1

        # Guardar historial
        iteraciones.append({
            'iter': n,
            'a': a,
            'b': b,
            'xr': xr,
            'error': error_calculado
        })

        # Criterio de parada
        if error_calculado < error_deseado and n > 1:
            break

        # Evaluar en qué subintervalo quedó la raíz
        fxr = f(xr)
        if fa * fxr < 0:
            b = xr
        elif fa * fxr > 0:
            a = xr
        else:
            break   # La función evaluada en xr es 0, es la raíz exacta

        xr_anterior = xr
        n += 1

    return iteraciones, xr
