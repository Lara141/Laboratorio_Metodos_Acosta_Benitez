"""Lectura, validación y evaluación segura de los datos de entrada."""

import ast
import math
import operator


_OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCIONES = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
}


def crear_funcion(expresion):
    """Convierte una expresión matemática permitida en f(x, y), sin eval()."""
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError as error:
        raise ValueError("La expresión no tiene una sintaxis válida.") from error

    def evaluar(nodo, x, y):
        if isinstance(nodo, ast.Expression):
            return evaluar(nodo.body, x, y)
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return nodo.value
        if isinstance(nodo, ast.Name):
            nombres = {"x": x, "y": y, "pi": math.pi, "e": math.e}
            if nodo.id in nombres:
                return nombres[nodo.id]
            raise ValueError(f"Nombre no permitido en la expresión: {nodo.id}")
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
            izquierda = evaluar(nodo.left, x, y)
            derecha = evaluar(nodo.right, x, y)
            return _OPERADORES[type(nodo.op)](izquierda, derecha)
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES_UNARIOS:
            return _OPERADORES_UNARIOS[type(nodo.op)](evaluar(nodo.operand, x, y))
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            nombre = nodo.func.id
            if nombre not in _FUNCIONES or nodo.keywords:
                raise ValueError(f"Función no permitida: {nombre}")
            argumentos = [evaluar(argumento, x, y) for argumento in nodo.args]
            return _FUNCIONES[nombre](*argumentos)
        raise ValueError(
            "La expresión contiene una operación no permitida. "
            "Use x, y, operaciones aritméticas y funciones como sqrt, sin o exp."
        )

    def validar(nodo):
        if isinstance(nodo, ast.Expression):
            validar(nodo.body)
        elif isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return
        elif isinstance(nodo, ast.Name):
            if nodo.id not in {"x", "y", "pi", "e"}:
                raise ValueError(f"Nombre no permitido en la expresión: {nodo.id}")
        elif isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
            validar(nodo.left)
            validar(nodo.right)
        elif isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES_UNARIOS:
            validar(nodo.operand)
        elif isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            if nodo.func.id not in _FUNCIONES or nodo.keywords:
                raise ValueError(f"Función no permitida: {nodo.func.id}")
            for argumento in nodo.args:
                validar(argumento)
        else:
            raise ValueError(
                "La expresión contiene una operación no permitida. "
                "Use x, y, operaciones aritméticas y funciones como sqrt, sin o exp."
            )

    validar(arbol)

    def funcion(x, y):
        resultado = float(evaluar(arbol, x, y))
        if not math.isfinite(resultado):
            raise ValueError("La función produjo un valor no finito.")
        return resultado

    return funcion


def leer_numero(mensaje):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
            if not math.isfinite(valor):
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Ingrese un número finito.")

def leer_entero_positivo(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
            if valor < 1:
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Ingrese un número entero mayor que cero.")


def solicitar_datos():
    print("\n--- DATOS DEL PROBLEMA ---")
    print("Ingrese la ecuación como y' = f(x, y), usando * para multiplicar.")
    print("Ejemplos: x**2 + y**2   |   3*x + 3*y   |   -0.06*sqrt(y)")

    while True:
        expresion = input("f(x, y) = ").strip()
        if not expresion:
            print("La expresión no puede quedar vacía.")
            continue
        try:
            funcion = crear_funcion(expresion)
            break
        except (ValueError, TypeError, ZeroDivisionError, OverflowError) as error:
            print(f"Expresión inválida: {error}")

    h = leer_numero("Tamaño de paso h (debe ser positivo): ")
    while h <= 0:
        print("El tamaño de paso debe ser mayor que cero.")
        h = leer_numero("Tamaño de paso h: ")

    print("\nMilne necesita cuatro valores iniciales (x, y), normalmente")
    print("obtenidos con Euler, Euler modificado o Runge-Kutta.")
    print("Se verificará que los 4 datos estén separados exactamente por h.")

    # Verificación de que los 4 datos iniciales son correctos (separados por h)
    while True:
        x_iniciales = []
        y_iniciales = []
        for i in range(4):
            xi = leer_numero(f"Ingrese x{i}: ")
            yi = leer_numero(f"Ingrese y{i}: ")
            x_iniciales.append(xi)
            y_iniciales.append(yi)
        
        datos_correctos = True
        for i in range(1, 4):
            diff = x_iniciales[i] - x_iniciales[i-1]
            if not math.isclose(diff, h, rel_tol=1e-5, abs_tol=1e-8):
                print(f"\nError: La distancia entre x{i-1} y x{i} es {diff:.6g}, pero h es {h}.")
                datos_correctos = False
                break
        
        if datos_correctos:
            print("¡Los 4 datos iniciales son válidos y equiespaciados!\n")
            break
        else:
            print("Por favor, ingrese los 4 datos iniciales nuevamente, respetando el tamaño de paso h.\n")

    # Ingreso del valor a predecir
    while True:
        objetivo = input("¿Qué valor desea predecir? (ej. x4, x5): ").strip().lower()
        if objetivo.startswith("x") and objetivo[1:].isdigit():
            indice_objetivo = int(objetivo[1:])
            if indice_objetivo < 4:
                print("Error: El índice a predecir debe ser 4 o mayor (x0 a x3 ya son conocidos).")
            else:
                pasos = indice_objetivo - 3
                break
        else:
            print("Formato inválido. Ingrese 'x' seguido de un número mayor o igual a 4 (ej. x4).")

    tolerancia = leer_numero("Tolerancia para las correcciones (debe ser positiva): ")
    while tolerancia <= 0:
        print("La tolerancia debe ser mayor que cero.")
        tolerancia = leer_numero("Tolerancia: ")

    max_correcciones = leer_entero_positivo("Cantidad máxima de correcciones permitidas por paso: ")

    return {
        "expresion": expresion,
        "funcion": funcion,
        "h": h,
        "x_iniciales": x_iniciales,
        "y_iniciales": y_iniciales,
        "pasos": pasos,
        "tolerancia": tolerancia,
        "max_correcciones": max_correcciones,
    }