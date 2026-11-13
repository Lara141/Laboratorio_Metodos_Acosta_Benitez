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

    x0 = leer_numero("Valor inicial x0: ")
    x_iniciales = [x0 + i * h for i in range(4)]

    print("\nMilne necesita cuatro valores iniciales de y, normalmente" )
    print("obtenidos con Euler, Euler modificado o Runge-Kutta.")
    y_iniciales = []
    for i, xi in enumerate(x_iniciales):
        yi = leer_numero(f"Ingrese y{i} para x{i} = {xi:.10g}: ")
        y_iniciales.append(yi)

    pasos = leer_entero_positivo("Cantidad de pasos de Milne que desea calcular: ")
    tolerancia = leer_numero("Tolerancia para las correcciones (debe ser positiva): ")
    while tolerancia <= 0:
        print("La tolerancia debe ser mayor que cero.")
        tolerancia = leer_numero("Tolerancia: ")

    return {
        "expresion": expresion,
        "funcion": funcion,
        "h": h,
        "x_iniciales": x_iniciales,
        "y_iniciales": y_iniciales,
        "pasos": pasos,
        "tolerancia": tolerancia,
    }
