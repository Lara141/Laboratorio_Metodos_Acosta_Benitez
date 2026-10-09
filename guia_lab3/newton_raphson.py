import sympy as sp

def ejecutar_newton_raphson(str_func, a, b, error_deseado, max_iter=100):

    # --- 0. CÁLCULO DE DERIVADAS
    x = sp.Symbol('x')
    expr = sp.sympify(str_func)
    f = sp.lambdify(x, expr, 'numpy')
    
    expr_diff = sp.diff(expr, x)
    df = sp.lambdify(x, expr_diff, 'numpy')
    str_df = str(expr_diff)
     
    expr_diff2 = sp.diff(expr_diff, x)
    d2f = sp.lambdify(x, expr_diff2, 'numpy')
    str_d2f = str(expr_diff2)

    # --- 1. MOSTRAR DERIVADAS ---
    print("\nDerivadas de la funcion")
    print(f"1ra derivada: f'(x) = {str_df}")
    print(f"2da derivada: f''(x) = {str_d2f}")
    
    # --- 2. VERIFICACIÓN DE CONDICIONES ---
    print("\nVERIFICACIÓN DE LAS CONDICIONES DE NEWTON-RAPHSON")
    print("="*50)
    
    # Condición 1: f(a) * f(b) < 0
    fa = f(a)
    fb = f(b)
    prod_ab = fa * fb
    print(f"\n1ra condicion: f(a) * f(b) < 0")
    print(f"f({a}) = {fa:.6f} | f({b}) = {fb:.6f}")
    print(f"Producto: {prod_ab:.6f}")
    
    if prod_ab < 0:
        print("Cumple: existe al menos una raíz en el intervalo.")
    elif prod_ab == 0:
        print(" ATENCIÓN Uno de los extremos es exactamente la raíz.")
    else:
        print("No cumple: como f(a) y f(b) tienen el mismo signo, no se garantiza la existencia de una raíz en este intervalo")
    
    # Condición 2: f'(x) != 0 (evaluamos en los extremos y posible cambio de signo)
    dfa = df(a)
    dfb = df(b)
    print(f"\n2da condicion: f'(x) != 0 en el intervalo")
    print(f"f'({a}) = {dfa:.6f} | f'({b}) = {dfb:.6f}")
    
    if dfa == 0 or dfb == 0:
        print("No cumple: La derivada es cero en uno de los extremos.")
    elif dfa * dfb < 0:
        print("No cumple:La derivada cambia de signo entre 'a' y 'b', lo que implica que f'(x) = 0 en algún punto intermedio.")
    else:
        print("Cumple: la primera derivada no es cero en los extremos y mantiene su signo.")
        
    # Condición 3: f''(x) para asegurar concavidad constante (no cambia de signo)
    d2fa = d2f(a)
    d2fb = d2f(b)
    print(f"\n3ra condicion: f''(x) mantiene su signo (Concavidad constante)")
    print(f"f''({a}) = {d2fa:.6f} | f''({b}) = {d2fb:.6f}")
    
    if d2fa * d2fb <= 0:
        print("No cumple: La segunda derivada cambia de signo o es cero. Existe un punto de inflexión en el intervalo.")
    else:
        print("Cumple: la segunda derivada mantiene el signo.")
    
    # --- 3. APLICAR CONDICIÓN DE FOURIER ---

    print("\nAplicamos la condición de Fourier: f(x0) * f''(x0) > 0")
    print("-"*50)
    
    prod_a = fa * d2fa
    print(f"Evaluando el extremo 'a' ({a}):")
    print(f"f({a}) * f''({a}) = {fa:.6f} * {d2fa:.6f} = {prod_a:.6f}")
    if prod_a > 0:
        print("Cumple: El resultado es mayor a cero.")
    else:
        print("No cumple: El resultado es menor o igual a cero.")
        
    prod_b = fb * d2fb
    print(f"\nEvaluando el extremo 'b' ({b}):")
    print(f"f({b}) * f''({b}) = {fb:.6f} * {d2fb:.6f} = {prod_b:.6f}")
    if prod_b > 0:
        print("Cumple: El resultado es mayor a cero.")
    else:
        print("No cumple: El resultado es menor o igual a cero.")
        
    # Selección de x0
    if prod_a > 0 and prod_b > 0:
        print(f"\nAmbos extremos cumplen Fourier. Se usará el extremo inferior x0 = {a} por defecto.")
        x0 = a
    elif prod_a > 0:
        x0 = a
        print(f"\nPor lo tanto, el punto de arranque óptimo es x0 = {x0}")
    elif prod_b > 0:
        x0 = b
        print(f"\nPor lo tanto, el punto de arranque óptimo es x0 = {x0}")
    else:
        print("\nATENCIÓN Ninguno de los extremos cumple la Condición de Fourier. El método podría divergir.")
        try:
            x0 = float(input(f"Ingresa el valor de arranque x0 manualmente (Sugerencia: {a} o {b}): "))
        except ValueError:
            print(f"> Valor inválido. Se utilizará x0 = {a} por defecto.")
            x0 = a

    # --- 4. ITERACIONES PASO A PASO ---
   
    print("\n INICIANDO ITERACIONES")
    print("="*50)
    iteraciones = []
    n = 1
    x_anterior = x0
    
    while n <= max_iter:
        fx = f(x_anterior)
        dfx = df(x_anterior)
        
        # Evitar división por cero
        if dfx == 0:
            print(f"\nERROR La primera derivada es cero en x{n-1} = {x_anterior}. El método ha fracasado.")
            break
            
        # Fórmula de Newton-Raphson 
        x_actual = x_anterior - (fx / dfx)
        
        # Calcular el error estimado absoluto
        error_calculado = abs(x_actual - x_anterior)
        
        # Imprimir desarrollo de la iteración con índices dinámicos (n-1 y n)
        print(f"\nIteración {n}")
        print(f"f(x{n-1}) = {fx:.6f}")
        print(f"f'(x{n-1}) = {dfx:.6f}")
        print(f"x{n} = x{n-1} - [f(x{n-1}) / f'(x{n-1})] = {x_anterior:.6f} - ({fx:.6f} / {dfx:.6f}) = {x_actual:.6f}")
        print(f"Error = | x{n} - x{n-1} | = | {x_actual:.6f} - {x_anterior:.6f} | = {error_calculado:.8f}")

        # Guardar historial agregando f(x) y f'(x) para la tabla final
        iteraciones.append({
            'iter': n,
            'x_ant': x_anterior,
            'fx': fx,
            'dfx': dfx,
            'x_act': x_actual,
            'error': error_calculado
        })

        # Criterio de parada
        if error_calculado < error_deseado:
            print(f"\nSe alcanzó la tolerancia deseada en la iteración {n}.")
            return iteraciones, x_actual

        x_anterior = x_actual
        n += 1

    print(f"\nADVERTENCIA Se alcanzó el máximo de {max_iter} iteraciones sin converger.")
    return iteraciones, x_anterior