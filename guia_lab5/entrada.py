import math


#Lectura y validación de valores individuales
def leer_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"Ingresá un entero mayor o igual que {minimo}.")
        except ValueError:
            print("Entrada inválida: ingresá un número entero.")


def leer_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje).strip().replace(",", "."))
            if math.isfinite(valor):
                return valor
            print("El valor debe ser finito.")
        except ValueError:
            print("Entrada inválida: ingresá un número real.")


#Lectura de datos para el problema
def leer_puntos(minimo=2):
    cantidad = leer_entero(f"Cantidad de pares de datos (mínimo {minimo}): ", minimo)
    x, y = [], []
    for i in range(cantidad):
        while True:
            try:
                texto = input(f"Punto {i + 1}, ingrese x_i e y_i separados por espacio: ")
                valores = [float(v.replace(",", ".")) for v in texto.split()]
                if len(valores) != 2:
                    print("Ingresá exactamente dos valores: x_i e y_i.")
                    continue
                if not all(math.isfinite(v) for v in valores):
                    print("Los valores deben ser finitos.")
                    continue
                x.append(valores[0])
                y.append(valores[1])
                break
            except ValueError:
                print("Fila inválida. Usá dos números separados por un espacio.")
    return x, y


def leer_grado(cantidad):
    maximo = cantidad - 1
    while True:
        texto = input(
            f"Grado del polinomio (Enter = usar todos los {cantidad} puntos, "
            f"o ingresá 0 a {maximo}): "
        ).strip()
        if texto == "":
            return maximo
        try:
            grado = int(texto)
            if 0 <= grado <= maximo:
                return grado
            print(f"El grado debe estar entre 0 y {maximo}.")
        except ValueError:
            print("Ingresá un entero o presioná Enter.")
