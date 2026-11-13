"""Programa principal para resolver ecuaciones diferenciales con Milne."""

from entrada import solicitar_datos
from milne import aplicar_milne


def mostrar_menu():
    print(" MENU")
    print("1. Metodo de Milne")
    print("2. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                datos = solicitar_datos()
                aplicar_milne(**datos)
            except (ValueError, TypeError, OverflowError, ZeroDivisionError) as error:
                print(f"\nNo se pudo completar el cálculo: {error}")
        elif opcion == "2":
            print("\nPrograma finalizado.")
            break
        else:
            print("Opción inválida. Ingrese 1 o 2.")


if __name__ == "__main__":
    main()
