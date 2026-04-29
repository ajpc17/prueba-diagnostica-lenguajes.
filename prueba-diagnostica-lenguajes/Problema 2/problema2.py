"""
Problema 2 - Validador de notacion FEN (Forsyth-Edwards Notation)
Curso: Lenguajes y Compiladores - UNEG
Implementacion: Python
"""

# ================================================================
#  CONSTANTES
# ================================================================
PIEZAS_VALIDAS  = set("rnbqkpRNBQKP")  # Letras validas para piezas
COLUMNAS_EP     = set("abcdefgh")       # Columnas validas para en passant
FILAS_EP        = {"3", "6"}            # Filas validas para en passant (w->6, b->3)


# ================================================================
#  PARTE 1: Validar la posicion del tablero
#  Ejemplo valido: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# ================================================================
def validar_tablero(tablero):
    """
    Reglas:
    - Debe haber exactamente 8 filas separadas por '/'
    - Cada fila debe sumar exactamente 8 casillas
    - Solo se permiten letras de piezas (rnbqkpRNBQKP) y numeros 1-8
    - Debe haber exactamente 1 rey blanco (K) y 1 rey negro (k)
    """
    filas = tablero.split("/")

    # Regla 1: Exactamente 8 filas
    if len(filas) != 8:
        return False, f"El tablero debe tener 8 filas, tiene {len(filas)}"

    reyes_blancos = 0
    reyes_negros  = 0

    for numero_fila, fila in enumerate(filas):
        casillas = 0

        for caracter in fila:
            if caracter.isdigit():
                # Un numero indica casillas vacias
                if not 1 <= int(caracter) <= 8:
                    return False, f"Numero invalido '{caracter}' en fila {numero_fila+1}"
                casillas += int(caracter)
            elif caracter in PIEZAS_VALIDAS:
                casillas += 1  # Una pieza ocupa exactamente 1 casilla
                if caracter == "K": reyes_blancos += 1
                if caracter == "k": reyes_negros  += 1
            else:
                return False, f"Caracter invalido '{caracter}' en fila {numero_fila+1}"

        # Regla 2: Cada fila debe sumar 8
        if casillas != 8:
            return False, f"Fila {numero_fila+1} suma {casillas} casillas, debe ser 8"

    # Regla 3: Exactamente un rey de cada color
    if reyes_blancos != 1:
        return False, f"Debe haber exactamente 1 rey blanco (K), hay {reyes_blancos}"
    if reyes_negros != 1:
        return False, f"Debe haber exactamente 1 rey negro (k), hay {reyes_negros}"

    return True, "Tablero valido"


# ================================================================
#  PARTE 2: Validar el turno
#  Solo puede ser 'w' (blancas) o 'b' (negras)
# ================================================================
def validar_turno(turno):
    if turno not in ("w", "b"):
        return False, f"Turno invalido '{turno}', debe ser 'w' o 'b'"
    return True, "Turno valido"


# ================================================================
#  PARTE 3: Validar disponibilidad de enroque
#  Puede ser '-' o cualquier combinacion de K Q k q sin repetir
#  Orden valido: siempre KQkq (los que apliquen)
# ================================================================
def validar_enroque(enroque):
    if enroque == "-":
        return True, "Sin enroque disponible"

    letras_validas = "KQkq"
    vistas = set()

    for c in enroque:
        if c not in letras_validas:
            return False, f"Caracter de enroque invalido '{c}'"
        if c in vistas:
            return False, f"Letra de enroque repetida '{c}'"
        vistas.add(c)

    # Verificar orden correcto: K antes de Q, K/Q antes de k/q
    orden = {c: i for i, c in enumerate("KQkq")}
    indices = [orden[c] for c in enroque]
    if indices != sorted(indices):
        return False, f"Orden de enroque incorrecto '{enroque}', debe seguir el orden KQkq"

    return True, "Enroque valido"


# ================================================================
#  PARTE 4: Validar casilla de en passant
#  Puede ser '-' o una casilla como e3 o e6
# ================================================================
def validar_en_passant(ep, turno):
    if ep == "-":
        return True, "Sin en passant"

    if len(ep) != 2:
        return False, f"En passant invalido '{ep}', debe ser una casilla de 2 caracteres"

    columna, fila = ep[0], ep[1]

    if columna not in COLUMNAS_EP:
        return False, f"Columna de en passant invalida '{columna}'"

    # Si es turno de blancas (w), capturan en fila 6; negras (b) en fila 3
    fila_esperada = "3" if turno == "w" else "6"
    if fila != fila_esperada:
        return False, f"Fila de en passant invalida '{fila}', con turno '{turno}' debe ser fila {fila_esperada}"

    return True, "En passant valido"


# ================================================================
#  PARTE 5: Validar contadores (medio movimientos y numero de jugada)
# ================================================================
def validar_contadores(medio_mov, num_jugada):
    # Medio movimientos: entero >= 0
    if not medio_mov.isdigit():
        return False, f"Medio movimientos invalido '{medio_mov}', debe ser un numero entero >= 0"

    # Numero de jugada: entero >= 1
    if not num_jugada.isdigit() or int(num_jugada) < 1:
        return False, f"Numero de jugada invalido '{num_jugada}', debe ser un entero >= 1"

    return True, "Contadores validos"


# ================================================================
#  FUNCION PRINCIPAL: Validar la cadena FEN completa
# ================================================================
def validar_fen(cadena):
    print("\n" + "=" * 60)
    print(f"  Validando FEN:")
    print(f"  '{cadena}'")
    print("=" * 60)

    # Paso 0: Separar por espacios → debe tener exactamente 6 partes
    partes = cadena.strip().split(" ")
    if len(partes) != 6:
        print(f"\n  ✗ ERROR: La cadena FEN debe tener 6 partes separadas por espacio")
        print(f"          Se encontraron {len(partes)} parte(s)")
        return False

    tablero, turno, enroque, ep, medio_mov, num_jugada = partes

    # Lista de validaciones a ejecutar en orden
    validaciones = [
        ("1. Tablero    ", validar_tablero(tablero)),
        ("2. Turno      ", validar_turno(turno)),
        ("3. Enroque    ", validar_enroque(enroque)),
        ("4. En passant ", validar_en_passant(ep, turno)),
        ("5. Contadores ", validar_contadores(medio_mov, num_jugada)),
    ]

    print()
    todo_valido = True

    for nombre, (valido, mensaje) in validaciones:
        simbolo = "✓" if valido else "✗"
        print(f"  {simbolo} {nombre}: {mensaje}")
        if not valido:
            todo_valido = False

    print()
    if todo_valido:
        print("  RESULTADO: ✓ Cadena FEN VALIDA")
    else:
        print("  RESULTADO: ✗ Cadena FEN INVALIDA")
    print("=" * 60)

    return todo_valido


# ================================================================
#  CASOS DE PRUEBA
# ================================================================
def ejecutar_pruebas():
    print("\n" + "=" * 60)
    print("  CASOS DE PRUEBA")
    print("=" * 60)

    casos = [
        # (cadena_fen, descripcion)
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "Posicion inicial del ajedrez"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e6 0 1",
            "Despues de 1.e4 con en passant valido"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "FEN valido estandar"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBN w KQkq - 0 1",
            "ERROR: fila incompleta (falta 1 casilla)"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1",
            "ERROR: turno invalido 'x'"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0",
            "ERROR: numero de jugada 0 (debe ser >= 1)"
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e3 0 1",
            "ERROR: en passant en fila incorrecta para turno blanco"
        ),
    ]

    resultados = []
    for fen, descripcion in casos:
        print(f"\n  >> {descripcion}")
        resultado = validar_fen(fen)
        resultados.append((descripcion, resultado))

    # Resumen final
    print("\n" + "=" * 60)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 60)
    for desc, res in resultados:
        simbolo = "✓" if res else "✗"
        print(f"  {simbolo} {desc}")


# ================================================================
#  MAIN
# ================================================================
def main():
    print("=" * 60)
    print("  PROBLEMA 2: Validador de Notacion FEN")
    print("  Lenguajes y Compiladores - UNEG  [version Python]")
    print("=" * 60)

    print("\n¿Que desea hacer?")
    print("  1) Validar una cadena FEN ingresada manualmente")
    print("  2) Ejecutar casos de prueba automaticos")
    opcion = input("\nOpcion (1/2): ").strip()

    if opcion == "1":
        cadena = input("\nIngrese la cadena FEN: ").strip()
        validar_fen(cadena)
    elif opcion == "2":
        ejecutar_pruebas()
    else:
        print("Opcion invalida.")


if __name__ == "__main__":
    main()
