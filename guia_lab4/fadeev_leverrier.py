from __future__ import annotations

import numpy as np


def fadeev_leverrier(A, tolerancia: float = 1e-10):
    A = np.array(A, dtype=float, copy=True)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada para hallar autovalores.")
    if not np.isfinite(A).all():
        raise ValueError("Todos los valores de A deben ser números finitos.")

    n = A.shape[0]
    identidad = np.eye(n)
    
    def fmt(val):
        if isinstance(val, (complex, np.complex128, np.complex64)):
            if abs(val.imag) < 1e-10:
                parte_real = 0.0 if val.real == 0 else val.real
                return f"{parte_real:g}"
            parte_real = 0.0 if val.real == 0 else val.real
            parte_imaginaria = 0.0 if val.imag == 0 else val.imag
            return f"{parte_real:g}{parte_imaginaria:+g}j"
        if val == 0:
            return "0"
        return f"{val:g}"

    def array2string_limpia(valores, precision=4):
        arreglo = np.real_if_close(np.asarray(valores), tol=1000)
        arreglo = np.array(arreglo, copy=True)
        umbral = 0.5 * 10 ** (-precision)

        def formato_real(valor):
            if abs(valor) <= umbral:
                return "0"
            return f"{valor:.{precision}f}".rstrip("0").rstrip(".")

        def formato_complejo(valor):
            real = formato_real(valor.real)
            if abs(valor.imag) <= umbral:
                return real
            signo = "+" if valor.imag > 0 else "-"
            imaginaria = formato_real(abs(valor.imag))
            return f"({real}{signo}{imaginaria}j)"

        if np.iscomplexobj(arreglo):
            parte_real = arreglo.real.copy()
            parte_imaginaria = arreglo.imag.copy()
            parte_real[np.abs(parte_real) <= umbral] = 0.0
            parte_imaginaria[np.abs(parte_imaginaria) <= umbral] = 0.0
            arreglo = parte_real + 1j * parte_imaginaria
            if np.all(parte_imaginaria == 0):
                arreglo = parte_real
        else:
            arreglo[np.abs(arreglo) <= umbral] = 0.0

        return np.array2string(
            arreglo,
            precision=precision,
            suppress_small=True,
            formatter={
                "float_kind": formato_real,
                "complex_kind": formato_complejo,
            },
        )

    print("\n" + "="*50)
    print("1. Primera matriz y primer coeficiente")
    print("="*50)
    B = A.copy()
    print("B_1 = A =")
    print(array2string_limpia(B))
    
    diag_B = np.diag(B)
    suma_traza = " + ".join([fmt(x) for x in diag_B])
    b_1 = np.trace(B)
    b_k_list = [b_1]
    coeficientes = [1.0, -b_1]
    
    print(f"\nb_1 = tr(B_1) = {suma_traza} = {fmt(b_1)}")

    print("\n" + "="*50)
    print("2. Matrices siguientes y sus coeficientes")
    print("="*50)
    
    for k in range(2, n + 1):
        print(f"\n--- Iteración k = {k} ---")
        print(f"Fórmula: B_{k} = A(B_{k-1} - b_{k-1}I)")
        
        B_prev = B.copy()
        b_prev = b_k_list[-1]
        
        bI = b_prev * identidad
        print(f"\nb_{k-1}I =")
        print(array2string_limpia(bI))
        
        resta = B_prev - bI
        print(f"\nResta (B_{k-1} - b_{k-1}I) =")
        print(array2string_limpia(resta))
        
        B = A @ resta
        print(f"\nResultado B_{k} = A * (B_{k-1} - b_{k-1}I) =")
        print(array2string_limpia(B))
        
        diag_B = np.diag(B)
        suma_traza = " + ".join([fmt(x) for x in diag_B])
        tr_B = np.trace(B)
        b_k = tr_B / k
        
        b_k_list.append(b_k)
        coeficientes.append(-b_k)
        print(f"\nb_{k} = (1/{k}) * tr(B_{k}) = (1/{k}) * ({suma_traza}) = {fmt(b_k)}")

    print("\n" + "="*50)
    print("3. Polinomio característico")
    print("="*50)

    print("\nPolinomio final igualado a cero:")
    terminos_final = [f"λ^{n}"]
    for i, b in enumerate(b_k_list, 1):
        potencia = n - i
        lam_str = f"λ^{potencia}" if potencia > 1 else ("λ" if potencia == 1 else "")
        signo = "+" if -b >= 0 else "-"
        terminos_final.append(f" {signo} {abs(b):g}{lam_str}")
    polinomio_final = "".join(terminos_final) + " = 0"
    if polinomio_final.startswith(" + "):
        polinomio_final = polinomio_final[3:]
    print(polinomio_final)

    print("\n" + "="*50)
    print("4. Autovalor y vector asociado")
    print("="*50)
    
    coeficientes_array = np.array(coeficientes, dtype=float)
    autovalores = np.roots(coeficientes_array)
    
    print(f"Resolviendo el polinomio característico, los autovalores son:")
    for idx, val in enumerate(autovalores, 1):
        print(f"λ_{idx} = {fmt(val)}")
        
    autovectores = np.zeros((n, n), dtype=complex)
    residuos = np.zeros(n, dtype=float)
    
    for j, valor in enumerate(autovalores):
        print(f"\n" + "-"*40)
        print(f"Para el autovalor λ = {fmt(valor)}")
        print("-"*40)
        print("Sistema homogéneo (A - λI)x = 0:")
        
        M = A.astype(complex) - valor * identidad
        print("\nMatriz resultante (A - λI):")
        print(array2string_limpia(M))
        
        print("\nAplicando eliminación de Gauss por filas:")
        M_gauss = M.copy()
        for col in range(n - 1):
            max_idx = col + np.argmax(np.abs(M_gauss[col:, col]))
            if np.abs(M_gauss[max_idx, col]) > tolerancia:
                if max_idx != col:
                    M_gauss[[col, max_idx]] = M_gauss[[max_idx, col]]
                    print(f"Intercambiando Fila {col+1} y Fila {max_idx+1}")
                for row in range(col + 1, n):
                    if np.abs(M_gauss[row, col]) > tolerancia:
                        factor = M_gauss[row, col] / M_gauss[col, col]
                        M_gauss[row, col:] -= factor * M_gauss[col, col:]
                        print(f"Fila {row+1} = Fila {row+1} - ({fmt(factor)}) * Fila {col+1}")
        
        print("\nMatriz escalonada resultante:")
        print(array2string_limpia(M_gauss))
        
        print("\nSustitución hacia atrás:")
        x = np.zeros(n, dtype=complex)
        
        x[-1] = 1.0
        print(f"Se toma la variable libre x_{n} = 1")
        
        for row in range(n - 2, -1, -1):
            if np.abs(M_gauss[row, row]) > tolerancia:
                suma = sum(M_gauss[row, c] * x[c] for c in range(row + 1, n))
                x[row] = -suma / M_gauss[row, row]
                
                terminos_str = " + ".join([f"({fmt(M_gauss[row, c])} * {fmt(x[c])})" for c in range(row + 1, n)])
                print(f"x_{row+1} = -[{terminos_str}] / ({fmt(M_gauss[row, row])}) = {fmt(x[row])}")
            else:
                x[row] = 1.0
                print(f"x_{row+1} = 1 (Tomada como variable libre adicional)")
                
        print(f"\nAutovalor: {fmt(valor)}")
        print("Vector asociado:")
        print(array2string_limpia(x))
        
        _, _, vh = np.linalg.svd(M)
        vector_svd = vh.conj().T[:, -1]
        norma = np.linalg.norm(vector_svd)
        if norma > 0:
            vector_svd = vector_svd / norma
            primero = next((v for v in vector_svd if abs(v) > tolerancia), None)
            if primero is not None:
                vector_svd *= np.exp(-1j * np.angle(primero))
            if np.max(np.abs(vector_svd.imag)) < tolerancia:
                vector_svd = vector_svd.real.astype(complex)
            autovectores[:, j] = vector_svd
        residuos[j] = float(np.linalg.norm(A @ vector_svd - valor * vector_svd))

    determinante = float(np.linalg.det(A))
    inversa = None
    if abs(determinante) > tolerancia:
        B_anterior = identidad.copy()
        for k in range(1, n):
            c_k = coeficientes[k]
            B_anterior = A @ B_anterior + c_k * identidad
        inversa = -B_anterior / coeficientes[-1]

    return {
        "coefficients": coeficientes_array,
        "eigenvalues": autovalores,
        "eigenvectors": autovectores,
        "residuals": residuos,
        "inverse": inversa,
        "determinant": determinante,
    }
