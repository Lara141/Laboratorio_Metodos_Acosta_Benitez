from time import perf_counter
from entrada import leer_float, leer_grado, leer_puntos
from lagrange import ErrorInterpolacion, evaluar_lagrange, polinomio_lagrange, seleccionar_nodos


# Presentación de resultados
# Imprime un encabezado numerado para organizar la salida en pantalla.
def seccion(numero, titulo):
    print(f"\n{numero}. {titulo}")
    print("-" * 58)

# Presenta en forma de tabla los valores X e Y de los nodos seleccionados.
def mostrar_nodos(x, y):
    print(f"{'i':>3} {'xi':>18} {'yi':>18}")
    for i, (xi, yi) in enumerate(zip(x, y)):
        print(f"{i:>3} {xi:>18.10g} {yi:>18.10g}")

# Muestra cada base de Lagrange, su contribución y la suma que da el resultado.
def mostrar_desarrollo(pasos, terminos, grado, x0, resultado, inicio=3):
    seccion(inicio, "DESARROLLO DE LOS TERMINOS")
    for paso in pasos:
        i = paso["indice"]
        print(f"\nL{i}({x0:g}) = [{paso['numerador']}] / [{paso['denominador']}]")
        print(f"L{i}({x0:g}) = {paso['base']:.12g}")
        print(f"y{i} * L{i}({x0:g}) = {paso['yi']:.12g} * {paso['base']:.12g} = {paso['contribucion']:.12g}")
    seccion(inicio + 1, "SUMA DE LOS TERMINOS")
    print(f"P{grado}({x0:g}) = " + " + ".join(f"y{i}*L{i}" for i in range(len(terminos))))
    print(f"P{grado}({x0:g}) = " + " + ".join(f"({t:.12g})" if t < 0 else f"{t:.12g}" for t in terminos))
    seccion(inicio + 2, "RESULTADO FINAL")
    print(f"P{grado}({x0:g}) = {resultado:.12g}")

# Solicita un valor conocido opcional para calcular los errores de interpolación.
def leer_referencia():
    while True:
        texto = input("Valor real/conocido para comparar (Enter si no se conoce): ").strip()
        if not texto:
            return None
        try:
            import math
            valor = float(texto.replace(",", "."))
            if math.isfinite(valor):
                return valor
        except ValueError:
            pass
        print("Ingresá un número real finito o presioná Enter.")

# Calcula e imprime los errores absoluto, relativo y porcentual.
def mostrar_errores(real, aproximado):
    absoluto = abs(real - aproximado)
    print(f"Valor de referencia: {real:.12g}")
    print(f"Error absoluto: {absoluto:.12g}")
    if real == 0:
        print("Error relativo y porcentual: no definidos (valor real igual a cero).")
    else:
        relativo = absoluto / abs(real)
        print(f"Error relativo: {relativo:.12g}")
        print(f"Error porcentual: {100 * relativo:.12g}%")


# Gestión de datos compartidos
# Valida una respuesta de sí/no y devuelve True o False.
def confirmar(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respondé S o N.")

# Permite reutilizar los puntos guardados o ingresar una nueva tabla.
def obtener_datos(datos, minimo=2):
    """Reutiliza los datos existentes o solicita una tabla nueva."""
    if datos is not None and len(datos[0]) >= minimo:
        print(f"\nHay {len(datos[0])} pares de datos guardados.")
        if confirmar("¿Deseás utilizar los mismos datos? (S/N): "):
            return datos
    elif datos is not None:
        print(f"\nEsta opción requiere al menos {minimo} puntos; los datos guardados no alcanzan.")
    return leer_puntos(minimo=minimo)


def repetir_calculo():
    return confirmar("\n¿Deseás interpolar otro valor de X con los mismos datos? (S/N): ")

# Opción 1: selecciona nodos, evalúa Lagrange y presenta los cálculos y errores.
def interpolacion_directa(x, y):
    while True:
        print("\n==== INTERPOLACION DIRECTA DE LAGRANGE ====")
        x0 = leer_float("Valor de X a interpolar: ")
        grado = leer_grado(len(x))
        try:
            inicio = perf_counter()
            x_sel, y_sel = seleccionar_nodos(x, y, x0, grado)
            resultado, pasos, terminos = evaluar_lagrange(x_sel, y_sel, x0)
            tiempo = perf_counter() - inicio
            seccion(1, "DATOS DEL PROBLEMA")
            print(f"X a interpolar: {x0:g} | Grado: {grado} | Puntos usados: {len(x_sel)}")
            seccion(2, "NODOS SELECCIONADOS AUTOMATICAMENTE")
            mostrar_nodos(x_sel, y_sel)
            mostrar_desarrollo(pasos, terminos, grado, x0, resultado)
            seccion(6, "ANALISIS DE ERROR")
            real = leer_referencia()
            if real is None:
                print("Sin valor real conocido, no se calcula el error verdadero.")
            else:
                mostrar_errores(real, resultado)
            print(f"\nTiempo de calculo (sin ingreso de datos): {tiempo:.9f} s")
        except (ValueError, OverflowError, FloatingPointError, ErrorInterpolacion) as error:
            print(f"No se pudo completar el calculo: {error}")
        if not repetir_calculo():
            break


# Opción 2: construcción y evaluación del polinomio
# Convierte los coeficientes del polinomio en una expresión legible de P(x).
def formatear_polinomio(coeficientes):
    partes = []
    for grado, coef in enumerate(coeficientes):
        if abs(coef) < 1e-12:
            continue
        factor = f"{abs(coef):.10g}"
        termino = factor if grado == 0 else f"{factor}*x" if grado == 1 else f"{factor}*x^{grado}"
        partes.append(("-" if coef < 0 else "+", termino))
    if not partes:
        return "P(x) = 0"
    signo, primero = partes[0]
    salida = ("-" if signo == "-" else "") + primero
    for signo, termino in partes[1:]:
        salida += f" {signo} {termino}"
    return "P(x) = " + salida

def mostrar_polinomio(x, y):
    while True:
        print("\n==== POLINOMIO INTERPOLANTE DE LAGRANGE ====")
        x0 = leer_float("Valor de X donde se evaluara el polinomio: ")
        grado = leer_grado(len(x))
        try:
            inicio = perf_counter()
            x_sel, y_sel = seleccionar_nodos(x, y, x0, grado)
            coeficientes = polinomio_lagrange(x_sel, y_sel)
            resultado, pasos, terminos = evaluar_lagrange(x_sel, y_sel, x0)
            tiempo = perf_counter() - inicio
            seccion(1, "DATOS DEL PROBLEMA")
            print(f"X a evaluar: {x0:g} | Grado: {grado}")
            seccion(2, "NODOS SELECCIONADOS AUTOMATICAMENTE")
            mostrar_nodos(x_sel, y_sel)
            seccion(3, "POLINOMIO INTERPOLANTE")
            print(formatear_polinomio(coeficientes))
            print("Coeficientes (orden ascendente):")
            for i, coef in enumerate(coeficientes):
                print(f"c{i} = {coef:.12g}")
            mostrar_desarrollo(pasos, terminos, grado, x0, resultado, inicio=4)
            print(f"\nTiempo de calculo (sin ingreso de datos): {tiempo:.9f} s")
        except (ValueError, OverflowError, FloatingPointError, ErrorInterpolacion) as error:
            print(f"No se pudo completar el calculo: {error}")
        if not repetir_calculo():
            break

# Opción 3:comparación de aproximaciones y análisis de errores
def analisis_errores(x, y):
    while True:
        print("\n==== ANALISIS DE ERRORES DE LAGRANGE ====")
        x0 = leer_float("Valor de X a interpolar: ")
        try:
            inicio = perf_counter()
            x2, y2 = seleccionar_nodos(x, y, x0, 2)
            valor2, pasos2, terminos2 = evaluar_lagrange(x2, y2, x0)
            x_completo, y_completo = seleccionar_nodos(x, y, x0, len(x) - 1)
            valor_completo, pasos_completo, terminos_completo = evaluar_lagrange(x_completo, y_completo, x0)
            tiempo = perf_counter() - inicio
            seccion(1, "DATOS DEL PROBLEMA")
            print(f"X a interpolar: {x0:g}")
            seccion(2, "NODOS PARA GRADO 2")
            mostrar_nodos(x2, y2)
            mostrar_desarrollo(pasos2, terminos2, 2, x0, valor2, inicio=3)
            seccion(6, f"NODOS PARA GRADO {len(x)-1}")
            mostrar_nodos(x_completo, y_completo)
            mostrar_desarrollo(pasos_completo, terminos_completo, len(x)-1, x0, valor_completo, inicio=7)
            seccion(10, "COMPARACION DE APROXIMACIONES")
            print(f"P2({x0:g}) = {valor2:.12g}")
            print(f"P{len(x)-1}({x0:g}) = {valor_completo:.12g}")
            print(f"Diferencia absoluta = {abs(valor_completo-valor2):.12g}")
            print("Esta diferencia NO equivale al error real ni garantiza una cota de error.")
            seccion(11, "ERRORES RESPECTO DE UN VALOR CONOCIDO")
            real = leer_referencia()
            if real is None:
                print("No se conoce el valor verdadero: solo se informa la diferencia comparativa.")
            else:
                print("\nPara el polinomio de grado 2:")
                mostrar_errores(real, valor2)
                print(f"\nPara el polinomio de grado {len(x)-1}:")
                mostrar_errores(real, valor_completo)
            print(f"\nTiempo de calculo (sin ingreso de datos): {tiempo:.9f} s")
        except (ValueError, OverflowError, FloatingPointError, ErrorInterpolacion) as error:
            print(f"No se pudo completar el calculo: {error}")
        if not repetir_calculo():
            break

# --- Menú principal ---
def main():
    datos = None
    while True:
        print("\n= MENU =")
        print("1. Interpolacion directa")
        print("2. Polinomio interpolante y evaluacion")
        print("3. Analisis de errores (comparacion de grados)")
        print("4. Ingresar nuevos datos")
        print("5. Salir")
        opcion = input("Elegi una opcion: ").strip()
        if opcion == "5":
            print("Fin del programa.")
            break
        if opcion not in ("1", "2", "3", "4"):
            print("Opcion invalida. Elegi del 1 al 5.")
            continue
        if opcion == "4":
            datos = leer_puntos()
            print(f"Se guardaron {len(datos[0])} pares de datos.")
            continue
        minimo = 4 if opcion == "3" else 2
        datos = obtener_datos(datos, minimo=minimo)
        if opcion == "1":
            interpolacion_directa(*datos)
        elif opcion == "2":
            mostrar_polinomio(*datos)
        else:
            analisis_errores(*datos)


if __name__ == "__main__":
    main()