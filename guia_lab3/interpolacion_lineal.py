def ejecutar_interpolacion_lineal(f, a, b, error_deseado, max_iter=100):
    print("\nVERIFICACIÓN DEL INTERVALO INICIAL")
    print("="*50)
    
    # 1. Evaluamos la función en los extremos iniciales
    fa = f(a)
    fb = f(b)
    prod_ab = fa * fb 
    
    print(f"Límite inferior 'a' = {a} -> f({a}) = {fa:.6f}")
    print(f"Límite superior 'b' = {b} -> f({b}) = {fb:.6f}")
    print(f"f(a) * f(b) = {prod_ab:.6f}")

    # 2. Verificaciones iniciales solicitadas
    if prod_ab == 0:
        print("\nATENCIÓN: f(a) * f(b) = 0, por lo cual una de las imágenes de los extremos es una raíz.")
        if fa == 0:
            print(f"-> f(a) = 0, entonces 'a' ({a}) es un extremo del intervalo de la raiz")
            return [], a
        elif fb == 0:
            print(f"-> f(b) = 0, entonces 'b' ({b}) es un extremo del intervalo de la raiz")
            return [], b
            
    elif prod_ab < 0:
        print("\nCumple: f(a) * f(b) < 0, hay un cambio de signo. Se cumple la condición y se puede empezar a iterar.")
        
    else: # prod_ab > 0
        print("\nNo cumple: f(a) * f(b) > 0, no hay cambios de signo por lo que no se cumple la condición.")
        print("-> NO se podrá iterar. Por favor, selecciona un nuevo intervalo en el menú.")
        # Retornamos listas vacías para que el main() vuelva al menú sin romper el código
        return [], None

    # --- 3. INICIO DE ITERACIONES ---
  
    print("\nINICIANDO ITERACIONES")
    print("="*50)
    
    iteraciones = []
    n = 1
    xn_anterior = None
    
    # Límite de iteraciones aplicado
    while n <= max_iter:
        # Evaluamos la función en los extremos actuales
        fa = f(a)
        fb = f(b)
        
        # Evitar división por cero
        if fb - fa == 0:
            print(f"\n[ERROR] f(b) - f(a) es cero ({fb:.6f} - {fa:.6f}), división por cero. El método fracasó.")
            break
            
        # Fórmula de Interpolación Lineal
        xn = (a * fb - b * fa) / (fb - fa)
        fxn = f(xn)
        
        # Calcular el error estimado absoluto
        if xn_anterior is not None:
            error_calculado = abs(xn - xn_anterior)
            err_str = f"Error = | x{n} - x{n-1} | = | {xn:.6f} - {xn_anterior:.6f} | = {error_calculado:.8f}"
        else:
            error_calculado = abs(b - a) # Error referencial para la primera iteración
            err_str = f"Error = | b - a | = | {b:.6f} - {a:.6f} | = {error_calculado:.8f} Error referencial inicial"

        # Toma de decisiones para el nuevo intervalo
        prod = fa * fxn
        if prod < 0:
            accion = f"f(a) * f(x{n}) = {fa:.6f} * {fxn:.6f} = {prod:.6f} < 0\nPor lo tanto, el nuevo límite superior (b) será x{n} = {xn:.6f}"
        elif prod > 0:
            accion = f"f(a) * f(x{n}) = {fa:.6f} * {fxn:.6f} = {prod:.6f} > 0\nPor lo tanto, el nuevo límite inferior (a) será x{n} = {xn:.6f}"
        else:
            accion = f"f(x{n}) = 0. Se encontró la raíz exacta."

        # Imprimir iteración paso a paso
        print(f"\nIteración {n}")
        print(f"Intervalo actual: [{a:.6f}, {b:.6f}]")
        print(f"f(a) = f({a:.6f}) = {fa:.6f}")
        print(f"f(b) = f({b:.6f}) = {fb:.6f}")
        print(f"x{n} = ({a:.6f} * {fb:.6f} - {b:.6f} * {fa:.6f}) / ({fb:.6f} - {fa:.6f}) = {xn:.6f}")
        print(f"f(x{n}) = f({xn:.6f}) = {fxn:.6f}")
        print(accion)
        print(err_str)

        # Guardar historial agregando fxn para la tabla final
        iteraciones.append({
            'iter': n,
            'a': a,
            'b': b,
            'xr': xn,
            'fxn': fxn,
            'error': error_calculado
        })

        # Criterio de parada por tolerancia
        if error_calculado < error_deseado and n > 1:
            print(f"\nSe alcanzó la tolerancia deseada en la iteración {n}.")
            break

        # Evaluar en qué subintervalo quedó la raíz para la siguiente vuelta
        if prod < 0:
            b = xn
        elif prod > 0:
            a = xn
        else:
            break   # La función evaluada en xn es 0, es la raíz exacta

        xn_anterior = xn
        n += 1

    if n > max_iter:
        print(f"\nADVERTENCIA Se alcanzó el máximo de {max_iter} iteraciones sin converger a la tolerancia.")

    return iteraciones, xn