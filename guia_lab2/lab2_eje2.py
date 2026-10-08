import math
import ast
import operator
import time

#Se encarga de redondear los valores a 3 digitos
def redondeo(valor, cifras_sig=3):
    if valor == 0:
        return 0.0
    magnitud = math.floor(math.log10(abs(valor)))
    return round(valor, cifras_sig - 1 - magnitud)

#Calcula los errores absolutos y relativos
def errores(exacto, aprox):
    e_abs = abs(exacto - aprox)
    e_rel = e_abs / abs(exacto) if exacto != 0 else 0
    return e_abs, e_rel

#Es una clase que se encarga de recorrer el arbol sintactico y aplicar el redondeo a cada operacion
class SimuladorAritmetica(ast.NodeVisitor):
    def __init__(self, cifras_sig=3):
        self.cifras = cifras_sig
        self.ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }

    #Esta funcion se ejecuta cada vez que el codigo encuentra un numero fuera de una operacion o parentecis
    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return redondeo(node.value, self.cifras)
        return node.value

    #Esta funcion se ejecuta cada vez que el codigo encuentra una operacion como suma, resta, multiplicacion o division
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        op = self.ops[type(node.op)]
        resultado_parcial = op(left, right)
        
        return redondeo(resultado_parcial, self.cifras)

    #Esta funcion se ejecuta cuando una operacion comienza con un numero negativo
    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return redondeo(-operand, self.cifras)
        return operand

def procesar_ecuacion():
    start_time = time.perf_counter()
    
    print("Ingrese la ecuacion matematica ej: (121 - 119) - 0.327 o (2/9)*(9/7)")
    print("Escriba 'salir' para terminar.\n")
    
    simulador = SimuladorAritmetica(cifras_sig=3)
    
    while True:
        expr = input("Ingrese la ecuacion: ").strip()
        
        if expr.lower() == 'salir':
            end_time = time.perf_counter()
            tiempo_total = end_time - start_time
            
            print("Finalizando programa...")
            print(f"Tiempo de ejecucion: {tiempo_total:.6f} segundos")
            break
            
        if not expr:
            continue
            
        try:
            # 1-Pasamos el string a un arbol sintatico
            arbol = ast.parse(expr, mode='eval')
            
            # 2-Calcula el valor exacto p
            exacto = round(eval(expr, {"__builtins__": None}), 5)
            
            # 3-Calcula el valor aproximado p*
            aprox = simulador.visit(arbol.body)
            
            # 4-Calcula los errores absolutos y relativos
            e_abs, e_rel = errores(exacto, aprox)
            
            # 5-Muestro los resultados por pantalla
            
            print(f"Análisis para: {expr}")
            print(f"Valor Exacto     : {exacto:.5f}")
            print(f"Valor Aproximado : {aprox}")
            print(f"Error Absoluto   : {e_abs}")
            print(f"Error Relativo   : {e_rel}")

            #mensaje de error por si no ingresan bien la ecuacion
        except SyntaxError:
            print("Error: Expresión matemática mal formada. Revise los paréntesis y operadores.\n")
        except KeyError:
            print("Error: Operador no soportado. Use solo +, -, *, /\n")
        except Exception as e:
            print(f"error inesperado: {e}\n")

if __name__ == "__main__":
    procesar_ecuacion()