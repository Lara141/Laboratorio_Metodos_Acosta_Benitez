"""Método predictor-corrector de Milne, con desarrollo paso a paso."""

import re


def _fmt(valor):
    valor = float(valor)
    if valor == 0:
        return "0"
    return f"{valor:.10g}"


def _mostrar_evaluacion(expresion, x, y, resultado, etiqueta):
    expresion_sustituida = re.sub(r"\bx\b", f"({_fmt(x)})", expresion)
    expresion_sustituida = re.sub(r"\by\b", f"({_fmt(y)})", expresion_sustituida)
    print(
        f"{etiqueta} = f(x={_fmt(x)}, y={_fmt(y)}) "
        f"= ({expresion}) -> ({expresion_sustituida}) = {_fmt(resultado)}"
    )


def aplicar_milne(expresion, funcion, h, x_iniciales, y_iniciales, pasos, tolerancia):
    """Calcula los pasos solicitados y muestra las sustituciones del método."""
    if h <= 0 or tolerancia <= 0:
        raise ValueError("h y la tolerancia deben ser mayores que cero.")
    if len(x_iniciales) != 4 or len(y_iniciales) != 4:
        raise ValueError("El método de Milne necesita exactamente cuatro valores iniciales.")

    xs = list(x_iniciales)
    ys = list(y_iniciales)
    fs = []

    print("\n" + "=" * 68)
    print("MÉTODO DE MILNE: PREDICTOR Y CORRECTOR")
    print("=" * 68)
    print(f"Ecuación: y' = {expresion}")
    print(f"Tamaño de paso: h = {_fmt(h)}")
    print(f"Tolerancia para las correcciones: {_fmt(tolerancia)}")
    print("\nValores iniciales proporcionados:")
    print(f"{'i':<5}{'x_i':<16}{'y_i':<18}f(x_i, y_i) = y'_i")
    print("-" * 68)

    for i in range(4):
        derivada = funcion(xs[i], ys[i])
        fs.append(derivada)
        print(f"{i:<5}{_fmt(xs[i]):<16}{_fmt(ys[i]):<18}{_fmt(derivada)}")
        _mostrar_evaluacion(expresion, xs[i], ys[i], derivada, f"f_{i}")

    max_correcciones = 50

    for _ in range(pasos):
        n = len(xs) - 1
        x_nuevo = xs[-1] + h

        print("\n" + "-" * 68)
        print(f"CÁLCULO DEL SIGUIENTE VALOR: x_{n + 1} = {_fmt(x_nuevo)}")
        print("-" * 68)

        # Fórmula predictora de Milne.
        f_n = fs[n]
        f_n_1 = fs[n - 1]
        f_n_2 = fs[n - 2]
        y_n_3 = ys[n - 3]
        termino_predictor = 2 * f_n - f_n_1 + 2 * f_n_2
        y_predicho = y_n_3 + (4 * h / 3) * termino_predictor

        print("\n1. Predictor de Milne:")
        print("y_(n+1)^p = y_(n-3) + (4h/3) * (2f_n - f_(n-1) + 2f_(n-2))")
        print(
            f"y_{n + 1}^p = {_fmt(y_n_3)} + (4*{_fmt(h)}/3) * "
            f"(2*{_fmt(f_n)} - {_fmt(f_n_1)} + 2*{_fmt(f_n_2)})"
        )
        print(
            f"y_{n + 1}^p = {_fmt(y_n_3)} + (4*{_fmt(h)}/3) * "
            f"({_fmt(termino_predictor)}) = {_fmt(y_predicho)}"
        )

        print("\n2. Corrector de Milne:")
        print("y_(n+1)^c = y_(n-1) + (h/3) * (f_(n+1) + 4f_n + f_(n-1))")

        y_usado = y_predicho
        y_corregido = y_predicho
        error_correccion = float("inf")
        convergio = False

        for iteracion in range(1, max_correcciones + 1):
            f_nuevo = funcion(x_nuevo, y_usado)
            _mostrar_evaluacion(
                expresion, x_nuevo, y_usado, f_nuevo,
                f"f_(n+1) en la corrección {iteracion}"
            )

            suma_corrector = f_nuevo + 4 * f_n + f_n_1
            y_corregido = ys[n - 1] + (h / 3) * suma_corrector
            error_correccion = abs(y_corregido - y_usado)

            print(
                f"y_{n + 1}^c = {_fmt(ys[n - 1])} + ({_fmt(h)}/3) * "
                f"({_fmt(f_nuevo)} + 4*{_fmt(f_n)} + {_fmt(f_n_1)})"
            )
            print(
                f"y_{n + 1}^c = {_fmt(ys[n - 1])} + ({_fmt(h)}/3) * "
                f"({_fmt(suma_corrector)}) = {_fmt(y_corregido)}"
            )
            print(
                f"Error de corrección = |{_fmt(y_corregido)} - "
                f"{_fmt(y_usado)}| = {_fmt(error_correccion)}"
            )

            if error_correccion < tolerancia:
                convergio = True
                break
            y_usado = y_corregido

        if not convergio:
            print(
                f"Aviso: se alcanzaron {max_correcciones} correcciones "
                "sin llegar a la tolerancia solicitada."
            )
            print("Se conservará la última aproximación calculada.")
        else:
            print(f"Se alcanzó la tolerancia en {iteracion} corrección(es).")

        xs.append(x_nuevo)
        ys.append(y_corregido)
        fs.append(funcion(x_nuevo, y_corregido))
        print(f"Resultado aceptado: y_{n + 1} = {_fmt(y_corregido)}")

    print("\n" + "=" * 68)
    print("TABLA FINAL DE RESULTADOS")
    print("=" * 68)
    print(f"{'i':<5}{'x_i':<18}{'y_i':<20}y'_i = f(x_i,y_i)")
    print("-" * 68)
    for i, (x, y, derivada) in enumerate(zip(xs, ys, fs)):
        print(f"{i:<5}{_fmt(x):<18}{_fmt(y):<20}{_fmt(derivada)}")

    return xs, ys, fs
