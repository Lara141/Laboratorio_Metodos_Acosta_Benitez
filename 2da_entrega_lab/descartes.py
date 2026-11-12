import numpy as np

def contar_cambios_signo(coeficientes):
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
    # coeficientes vienen en orden: [a_n, a_{n-1}, ..., a_0]
    n = len(coeficientes) - 1
    
    print("\n" + "="*50)
    print("REGLA DE LOS SIGNOS DE DESCARTES")
    print("="*50)
    
    # Raíces positivas p(λ)
    cambios_pos = contar_cambios_signo(coeficientes)
    print("Análisis para raíces positivas p(λ):")
    print(f"Coeficientes: {[round(c, 4) for c in coeficientes]}")
    print(f"Cambios de signo encontrados: {cambios_pos}")
    print(f"-> Podría haber hasta {cambios_pos} raíz/raíces real(es) positiva(s).")
    
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
    print(f"Coeficientes de p(-λ): {[round(c, 4) for c in coef_neg]}")
    print(f"Cambios de signo encontrados: {cambios_neg}")
    print(f"-> Podría haber hasta {cambios_neg} raíz/raíces real(es) negativa(s).")
    
    print("\nNota: La regla de Descartes indica una cantidad máxima posible de raíces reales, no la cantidad exacta. Si el polinomio tiene autovalores complejos, estos métodos no los detectarán.")