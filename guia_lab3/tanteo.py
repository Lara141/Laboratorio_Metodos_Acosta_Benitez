import numpy as np

def tabla_tanteo(f, inicio, fin, paso):
    """
    Evalúa la función f en el rango [inicio, fin] con un incremento 'paso'.
    Devuelve la tabla de valores generada y una lista con todos los intervalos 
    [a, b] donde se detecta un cambio de signo (lo que indica una raíz).
    """
    valores = []
    # Generamos los valores de x basándonos en el inicio, fin y paso
    x_vals = np.arange(inicio, fin + paso, paso)
    
    # Ahora usamos una lista para guardar múltiples intervalos en lugar de una sola variable
    intervalos_raiz = []

    for i in range(len(x_vals)):
        x_actual = x_vals[i]
        y_actual = f(x_actual)
        valores.append((x_actual, y_actual))

        # Si estamos en el primer valor y es exactamente 0, es una raíz
        if i == 0 and y_actual == 0:
            intervalos_raiz.append((x_actual, x_actual))
            
        # Comparamos el signo del valor actual con el anterior para buscar raíces
        elif i > 0:
            x_ant, y_ant = valores[i-1]
            if y_ant * y_actual < 0:
                intervalos_raiz.append((x_ant, x_actual))
            elif y_actual == 0:
                # Si y_actual es exactamente 0, encontramos una raíz exacta
                intervalos_raiz.append((x_actual, x_actual))

    return valores, intervalos_raiz