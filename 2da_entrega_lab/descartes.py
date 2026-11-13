#Aplicación de la regla de los signos de Descartes.
#Este módulo analiza la cantidad máxima de raíces reales positivas y negativas de
#un polinomio a partir de los cambios de signo en sus coeficientes.
import numpy as np

def contar_cambios_signo(coeficientes):
    #Cuenta la cantidad de cambios de signo en una secuencia de coeficientes.
    #Args:
     #   coeficientes: Lista o array con los coeficientes del polinomio.
    #Returns:
     #   Cantidad de variaciones de signo ignorando coeficientes nulos.
    
    cambios = 0
    prev_signo = None
    for c in coeficientes:
        if abs(c) > 1e-10:
            signo = np.sign(c)
            if prev_signo is not None and signo != prev_signo:
                cambios += 1
            prev_signo = signo
    return cambios


def analisis_descartes(coeficientes):
    #Aplica la regla de Descartes para analizar la cantidad de raíces reales.
    #Args:
     #   coeficientes: Coeficientes del polinomio en orden descendente de potencia.
    #Returns:
     #   Tupla (cambios_pos, cambios_neg) con el número máximo de raíces reales
      #  positivas y negativas, respectivamente.
      
    n = len(coeficientes) - 1

    print("REGLA DE LOS SIGNOS DE DESCARTES")
    print("-"*50)

    # Raíces positivas p(λ)
    cambios_pos = contar_cambios_signo(coeficientes)
    print("Análisis para raíces positivas p(λ):")
    print(f"-> Según los cambios de signo en p(λ), podría haber hasta {cambios_pos} raíz/raíces real(es) positiva(s).")

    # Raíces negativas p(-λ)
    coef_neg = []
    for i, c in enumerate(coeficientes):
        potencia = n - i
        if potencia % 2 != 0:
            coef_neg.append(-c)
        else:
            coef_neg.append(c)

    cambios_neg = contar_cambios_signo(coef_neg)
    print("\nAnálisis para raíces negativas p(-λ):")
    print(f" Según los cambios de signo en p(-λ), podría haber hasta {cambios_neg} raíz/raíces real(es) negativa(s).")

    return cambios_pos, cambios_neg