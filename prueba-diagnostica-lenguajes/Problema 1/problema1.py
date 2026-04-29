"""
Problema 1 - Triángulo de Pascal y Evaluación de Polinomio (x+1)^n
Curso: Lenguajes y Compiladores - UNEG
Implementación: Python con memoria dinámica (listas dinámicas)
"""

import time
import sys


def format_number(num):
    """
    Formatea un número para mostrarlo como entero si es entero, de lo contrario como float.
    """
    if num == int(num):
        return str(int(num))
    else:
        return str(num)


def generar_coeficientes(n):
    """
    Genera los coeficientes del polinomio (x+1)^n usando el Triángulo de Pascal.
    Usa listas de Python como equivalente a memoria dinámica.
    Retorna una lista con los n+1 coeficientes.
    """
    # Caso base
    if n == 0:
        return [1]

    # Inicializamos con la primera fila del triángulo: [1]
    fila_anterior = [1]

    for i in range(1, n + 1):
        # Creamos la nueva fila dinámicamente
        fila_actual = [0] * (i + 1)
        fila_actual[0] = 1          # Primer elemento siempre es 1
        fila_actual[i] = 1          # Último elemento siempre es 1

        # Los elementos intermedios se calculan sumando los dos de arriba
        for j in range(1, i):
            fila_actual[j] = fila_anterior[j - 1] + fila_anterior[j]

        fila_anterior = fila_actual  # La fila actual pasa a ser la anterior

    return fila_anterior


def mostrar_polinomio(coeficientes, n):
    """
    Construye y muestra la representación textual del polinomio.
    Ejemplo para n=3: x^3 + 3x^2 + 3x + 1
    """
    terminos = []

    for i, coef in enumerate(coeficientes):
        # El exponente del término actual va de n hasta 0
        exponente = n - i

        if coef == 0:
            continue  # Saltamos términos con coeficiente 0

        if exponente == 0:
            # Término independiente (sin x)
            terminos.append(str(coef))
        elif exponente == 1:
            # Término lineal
            if coef == 1:
                terminos.append("x")
            else:
                terminos.append(f"{coef}x")
        else:
            # Término con potencia
            if coef == 1:
                terminos.append(f"x^{exponente}")
            else:
                terminos.append(f"{coef}x^{exponente}")

    return " + ".join(terminos) if terminos else "0"


def evaluar_polinomio_pasos(coeficientes, n, x):
    """
    Evalúa f(x) = (x+1)^n usando los coeficientes generados.
    Muestra el proceso paso a paso:
    Usa el Esquema de Horner para evaluar eficientemente.
    f(x) = c0*x^n + c1*x^(n-1) + ... + cn
    """
    print(f"\n{'='*55}")
    print(f"  Evaluación paso a paso de f({format_number(x)}) = ({format_number(x)}+1)^{n}")
    print(f"{'='*55}")

    if n == 0:
        print(f"  f({x}) = 1")
        return 1

    print(f"\n  Polinomio: f(x) = {mostrar_polinomio(coeficientes, n)}")
    print(f"\n  Sustituyendo x = {format_number(x)}:")
    print()

    resultado = 0
    terminos_evaluados = []

    for i, coef in enumerate(coeficientes):
        exponente = n - i
        valor_termino = coef * (x ** exponente)
        terminos_evaluados.append(valor_termino)

        if exponente == 0:
            print(f"    Término {i+1}: {coef} × {format_number(x)}^0 = {coef} × 1 = {format_number(valor_termino)}")
        elif exponente == 1:
            print(f"    Término {i+1}: {coef} × {format_number(x)}^1 = {coef} × {format_number(x)} = {format_number(valor_termino)}")
        else:
            print(f"    Término {i+1}: {coef} × {format_number(x)}^{exponente} = {coef} × {format_number(x**exponente)} = {format_number(valor_termino)}")

        resultado += valor_termino

    print()
    suma_str = " + ".join(format_number(t) for t in terminos_evaluados)
    print(f"  Suma total: {suma_str}")
    print(f"\n  ∴ f({format_number(x)}) = {format_number(resultado)}")
    print(f"  Verificación directa: ({format_number(x)}+1)^{n} = {format_number((x+1)**n)}")
    print(f"{'='*55}")

    return resultado


def medir_tiempo_n100():
    """
    Mide el tiempo de ejecución para n=100 y guarda resultados en archivo.
    """
    n = 100
    print(f"\nMidiendo tiempo de ejecución para n={n}...")

    inicio = time.perf_counter()
    coeficientes = generar_coeficientes(n)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    # Guardamos en archivo TXT
    with open("resultado_n100.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"Resultado para n={n}\n")
        archivo.write(f"{'='*60}\n")
        archivo.write(f"Tiempo de ejecución: {tiempo_ms:.6f} ms\n")
        archivo.write(f"Número de coeficientes generados: {len(coeficientes)}\n\n")
        archivo.write("Coeficientes (desde x^100 hasta x^0):\n")
        for i, c in enumerate(coeficientes):
            archivo.write(f"  C({i}) = {c}\n")

    print(f"  Tiempo: {tiempo_ms:.6f} ms")
    print(f"  Resultados guardados en 'resultado_n100.txt'")

    return tiempo_ms, coeficientes


def main():
    print("=" * 55)
    print("  PROBLEMA 1: Triángulo de Pascal - (x+1)^n")
    print("  Lenguajes y Compiladores - UNEG")
    print("=" * 55)

    # --- Parte a): Generar y mostrar el polinomio ---
    try:
        n = int(input("\nIngrese el valor de n (entero no negativo): "))
        if n < 0:
            print("Error: n debe ser no negativo.")
            sys.exit(1)
    except ValueError:
        print("Error: ingrese un número entero válido.")
        sys.exit(1)

    print(f"\n  Generando coeficientes para (x+1)^{n}...\n")
    coeficientes = generar_coeficientes(n)

    print(f"  Coeficientes obtenidos (Triángulo de Pascal, fila {n}):")
    print(f"  {coeficientes}")

    polinomio = mostrar_polinomio(coeficientes, n)
    print(f"\n  Polinomio resultante:")
    print(f"  f(x) = (x+1)^{n} = {polinomio}")

    # --- Parte b): Evaluar el polinomio para x dado ---
    try:
        x = float(input(f"\nIngrese el valor de x para evaluar f(x) = (x+1)^{n}: "))
    except ValueError:
        print("Error: ingrese un número válido.")
        sys.exit(1)

    evaluar_polinomio_pasos(coeficientes, n, x)

    # --- Medición de tiempo para n=100 ---
    print("\n" + "=" * 55)
    print("  MEDICIÓN DE TIEMPO PARA n=100")
    print("=" * 55)
    medir_tiempo_n100()

    print("\n¡Programa finalizado exitosamente!")


if __name__ == "__main__":
    main()
