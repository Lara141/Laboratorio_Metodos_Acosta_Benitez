import math
import numpy as np
from numpy.polynomial import Polynomial


#Error específico del método 
class ErrorInterpolacion(ValueError):
    """Indica que los datos no cumplen las condiciones de interpolación."""


# Validación de nodos y valores
# Convierte los datos a arreglos y valida tamaño, finitud y unicidad.
def _validar_datos(nodos, valores):
    x = np.asarray(nodos, dtype=float).reshape(-1)
    y = np.asarray(valores, dtype=float).reshape(-1)
    if x.size != y.size or x.size == 0:
        raise ErrorInterpolacion("Debe haber al menos un punto y la misma cantidad de X e Y.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ErrorInterpolacion("Los datos deben ser finitos.")
    if np.unique(x).size != x.size:
        raise ErrorInterpolacion("Los valores de X no pueden repetirse.")
    return x, y


# Selección de nodos cercanos al objetivo 
def seleccionar_nodos(nodos, valores, objetivo, grado):
    x, y = _validar_datos(nodos, valores)
    if not isinstance(grado, (int, np.integer)) or not 0 <= grado < x.size:
        raise ErrorInterpolacion("El grado debe estar entre 0 y cantidad de puntos - 1.")
    cantidad = grado + 1
    if objetivo is None:
        indices = np.arange(cantidad)
    else:
        if not math.isfinite(float(objetivo)):
            raise ErrorInterpolacion("El valor a interpolar debe ser finito.")
        indices = np.argsort(np.abs(x - objetivo), kind="stable")[:cantidad]
        indices = indices[np.argsort(x[indices], kind="stable")]
    return x[indices], y[indices]


# Evaluación numérica del interpolante
def evaluar_lagrange(nodos, valores, objetivo):
    x, y = _validar_datos(nodos, valores)
    objetivo = float(objetivo)
    if not math.isfinite(objetivo):
        raise ErrorInterpolacion("El valor a interpolar debe ser finito.")
    pasos, terminos = [], []
    for i in range(len(x)):
        numeradores, denominadores = [], []
        base = 1.0
        for j in range(len(x)):
            if j == i:
                continue
            numeradores.append(f"({objetivo:.10g} - {x[j]:.10g})")
            denominadores.append(f"({x[i]:.10g} - {x[j]:.10g})")
            base *= (objetivo - x[j]) / (x[i] - x[j])
        contribucion = float(y[i] * base)
        terminos.append(contribucion)
        pasos.append({
            "indice": i,
            "numerador": " * ".join(numeradores) or "1",
            "denominador": " * ".join(denominadores) or "1",
            "base": float(base),
            "yi": float(y[i]),
            "contribucion": contribucion,
        })
    return float(sum(terminos)), pasos, terminos


# Construcción simbólica mediante coeficientes
def polinomio_lagrange(nodos, valores):
    """Devuelve los coeficientes de P(x), ordenados por potencia ascendente."""
    x, y = _validar_datos(nodos, valores)
    polinomio = Polynomial([0.0])
    for i in range(len(x)):
        base = Polynomial([1.0])
        denominador = 1.0
        for j in range(len(x)):
            if i != j:
                base *= Polynomial([-x[j], 1.0])
                denominador *= x[i] - x[j]
        polinomio += y[i] / denominador * base
    return polinomio.coef
