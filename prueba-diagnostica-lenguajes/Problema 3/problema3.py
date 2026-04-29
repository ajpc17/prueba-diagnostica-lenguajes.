"""
Problema 3 - Traductor de Palabras Reservadas de C al Español
Unidad curricular: Lenguajes y Compiladores - UNEG
Implementacion: Python con memoria dinamica (listas y diccionarios dinamicos)

Funcionamiento:
  1. Carga un archivo .c en memoria dinamica (lista de caracteres)
  2. Recorre el texto identificando tokens (palabras)
  3. Si el token es una palabra reservada de C, la traduce al español
  4. Muestra el resultado original vs traducido
"""

import sys
import os


# ================================================================
#  DICCIONARIO DE PALABRAS RESERVADAS DE C Y SU TRADUCCION
#  Cargado dinamicamente en memoria como un dict de Python
# ================================================================
def crear_diccionario_reservadas():
    """
    Retorna un diccionario con todas las palabras reservadas de C
    y su equivalente en español.
    Se crea dinamicamente en tiempo de ejecucion.
    """
    reservadas = {
        "auto"     : "automatico",
        "break"    : "romper",
        "case"     : "caso",
        "char"     : "caracter",
        "const"    : "constante",
        "continue" : "continuar",
        "default"  : "defecto",
        "do"       : "hacer",
        "double"   : "doble",
        "else"     : "sino",
        "enum"     : "enumeracion",
        "extern"   : "externo",
        "float"    : "flotante",
        "for"      : "para",
        "goto"     : "ir_a",
        "if"       : "si",
        "int"      : "entero",
        "long"     : "largo",
        "register" : "registro",
        "return"   : "retornar",
        "short"    : "corto",
        "signed"   : "con_signo",
        "sizeof"   : "tamano_de",
        "static"   : "estatico",
        "struct"   : "estructura",
        "switch"   : "segun",
        "typedef"  : "definir_tipo",
        "union"    : "union_c",
        "unsigned" : "sin_signo",
        "void"     : "vacio",
        "volatile" : "volatil",
        "while"    : "mientras",
    }
    return reservadas


# ================================================================
#  CARGAR ARCHIVO EN MEMORIA DINAMICA
#  Lee el archivo caracter por caracter y lo guarda en una lista
#  (equivalente a malloc en C — la lista crece dinamicamente)
# ================================================================
def cargar_archivo_memoria(ruta):
    """
    Carga el contenido del archivo en una lista de caracteres.
    En Python las listas son dinamicas — equivalen al malloc de C.

    Retorna:
        lista de caracteres si el archivo existe
        None si hubo error
    """
    if not os.path.exists(ruta):
        print(f"  ERROR: El archivo '{ruta}' no existe.")
        return None

    memoria = []  # Lista dinamica — crece automaticamente

    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as archivo:
            while True:
                caracter = archivo.read(1)   # Leer un caracter a la vez
                if not caracter:
                    break
                memoria.append(caracter)     # Agregar a memoria dinamica
    except Exception as e:
        print(f"  ERROR al leer el archivo: {e}")
        return None

    return memoria


# ================================================================
#  TOKENIZADOR
#  Recorre la memoria y extrae tokens (palabras, simbolos, etc.)
#  Ignora el contenido de strings y comentarios
# ================================================================
def tokenizar(memoria):
    """
    Recorre la lista de caracteres y produce una lista de tokens.
    Cada token es un dict con:
        - 'texto'  : el texto del token
        - 'tipo'   : 'palabra', 'string', 'comentario', 'otro'
        - 'linea'  : numero de linea donde aparece

    La lista de tokens se crea dinamicamente.
    """
    tokens = []      # Lista dinamica de tokens
    i      = 0
    linea  = 1
    n      = len(memoria)

    while i < n:
        c = memoria[i]

        # ── Salto de linea ──────────────────────────────────────
        if c == '\n':
            tokens.append({'texto': '\n', 'tipo': 'otro', 'linea': linea})
            linea += 1
            i += 1

        # ── Comentario de bloque: /* ... */ ─────────────────────
        elif c == '/' and i + 1 < n and memoria[i + 1] == '*':
            comentario = []
            linea_inicio = linea
            i += 2
            while i < n:
                if memoria[i] == '\n':
                    linea += 1
                if memoria[i] == '*' and i + 1 < n and memoria[i + 1] == '/':
                    i += 2
                    break
                comentario.append(memoria[i])
                i += 1
            tokens.append({
                'texto': '/*' + ''.join(comentario) + '*/',
                'tipo' : 'comentario',
                'linea': linea_inicio
            })

        # ── Comentario de linea: // ... ─────────────────────────
        elif c == '/' and i + 1 < n and memoria[i + 1] == '/':
            comentario = []
            linea_inicio = linea
            i += 2
            while i < n and memoria[i] != '\n':
                comentario.append(memoria[i])
                i += 1
            tokens.append({
                'texto': '//' + ''.join(comentario),
                'tipo' : 'comentario',
                'linea': linea_inicio
            })

        # ── String: "..." ────────────────────────────────────────
        elif c == '"':
            string = ['"']
            i += 1
            while i < n and memoria[i] != '"':
                if memoria[i] == '\\':   # Caracter de escape
                    string.append(memoria[i])
                    i += 1
                if i < n:
                    string.append(memoria[i])
                i += 1
            if i < n:
                string.append('"')
                i += 1
            tokens.append({'texto': ''.join(string), 'tipo': 'string', 'linea': linea})

        # ── Caracter: '...' ──────────────────────────────────────
        elif c == "'":
            char_lit = ["'"]
            i += 1
            while i < n and memoria[i] != "'":
                char_lit.append(memoria[i])
                i += 1
            if i < n:
                char_lit.append("'")
                i += 1
            tokens.append({'texto': ''.join(char_lit), 'tipo': 'string', 'linea': linea})

        # ── Palabra o identificador ──────────────────────────────
        elif c.isalpha() or c == '_':
            palabra = []
            while i < n and (memoria[i].isalnum() or memoria[i] == '_'):
                palabra.append(memoria[i])
                i += 1
            tokens.append({
                'texto': ''.join(palabra),
                'tipo' : 'palabra',
                'linea': linea
            })

        # ── Numero ───────────────────────────────────────────────
        elif c.isdigit():
            numero = []
            while i < n and (memoria[i].isdigit() or memoria[i] == '.'):
                numero.append(memoria[i])
                i += 1
            tokens.append({'texto': ''.join(numero), 'tipo': 'numero', 'linea': linea})

        # ── Cualquier otro caracter (operadores, llaves, etc.) ───
        else:
            tokens.append({'texto': c, 'tipo': 'otro', 'linea': linea})
            i += 1

    return tokens


# ================================================================
#  TRADUCIR TOKENS
#  Recorre los tokens y sustituye palabras reservadas por su
#  traduccion al español
# ================================================================
def traducir_tokens(tokens, diccionario):
    """
    Recorre la lista de tokens.
    Si el token es una palabra reservada, lo traduce.
    Retorna:
        - lista de tokens traducidos
        - lista de hallazgos: (linea, palabra_original, traduccion)
    """
    traducidos = []
    hallazgos  = []   # Lista dinamica de palabras encontradas

    for token in tokens:
        if token['tipo'] == 'palabra' and token['texto'] in diccionario:
            traduccion = diccionario[token['texto']]
            hallazgos.append({
                'linea'    : token['linea'],
                'original' : token['texto'],
                'traduccion': traduccion
            })
            traducidos.append({
                'texto': traduccion,
                'tipo' : 'reservada',
                'linea': token['linea']
            })
        else:
            traducidos.append(token)

    return traducidos, hallazgos


# ================================================================
#  RECONSTRUIR TEXTO
#  Convierte la lista de tokens de vuelta a texto plano
# ================================================================
def reconstruir_texto(tokens):
    return ''.join(t['texto'] for t in tokens)


# ================================================================
#  MOSTRAR REPORTE
# ================================================================
def mostrar_reporte(ruta, memoria, hallazgos, texto_original, texto_traducido):
    print("\n" + "=" * 65)
    print("  REPORTE DE TRADUCCION")
    print("=" * 65)
    print(f"  Archivo        : {ruta}")
    print(f"  Tamaño en mem  : {len(memoria)} caracteres")
    print(f"  Palabras reser.: {len(hallazgos)} encontradas")
    print("=" * 65)

    if not hallazgos:
        print("\n  No se encontraron palabras reservadas de C.")
    else:
        print(f"\n  {'Linea':<8} {'Palabra C':<15} {'Traduccion'}")
        print(f"  {'-'*8} {'-'*15} {'-'*20}")
        for h in hallazgos:
            print(f"  {h['linea']:<8} {h['original']:<15} {h['traduccion']}")

    print("\n" + "=" * 65)
    print("  CODIGO ORIGINAL")
    print("=" * 65)
    # Mostrar con numeros de linea
    for i, linea in enumerate(texto_original.split('\n'), 1):
        print(f"  {i:3d} | {linea}")

    print("\n" + "=" * 65)
    print("  CODIGO TRADUCIDO")
    print("=" * 65)
    for i, linea in enumerate(texto_traducido.split('\n'), 1):
        print(f"  {i:3d} | {linea}")

    print("=" * 65)


# ================================================================
#  CREAR ARCHIVO DE PRUEBA
#  Si el usuario no tiene un archivo .c, generamos uno de ejemplo
# ================================================================
def crear_archivo_prueba():
    contenido = """\
#include <stdio.h>
#include <stdlib.h>

/* Funcion que calcula el factorial de n */
int factorial(int n) {
    if (n <= 0) {
        return 1;
    }
    int resultado = 1;
    int i;
    for (i = 1; i <= n; i++) {
        resultado = resultado * i;
    }
    return resultado;
}

/* Funcion que verifica si un numero es par */
int es_par(int numero) {
    if (numero % 2 == 0) {
        return 1;
    } else {
        return 0;
    }
}

int main() {
    int n = 5;
    int i;

    // Calcular factoriales del 1 al n
    for (i = 1; i <= n; i++) {
        int f = factorial(i);
        printf("factorial(%d) = %d\\n", i, f);
    }

    // Verificar pares e impares
    int contador = 0;
    while (contador < n) {
        if (es_par(contador)) {
            printf("%d es par\\n", contador);
        } else {
            printf("%d es impar\\n", contador);
        }
        contador++;
    }

    // Uso de switch
    int dia = 3;
    switch (dia) {
        case 1:
            printf("Lunes\\n");
            break;
        case 2:
            printf("Martes\\n");
            break;
        case 3:
            printf("Miercoles\\n");
            break;
        default:
            printf("Otro dia\\n");
            break;
    }

    return 0;
}
"""
    ruta = "programa_prueba.c"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"  Archivo de prueba creado: '{ruta}'")
    return ruta


# ================================================================
#  MAIN
# ================================================================
def main():
    print("=" * 65)
    print("  PROBLEMA 3: Traductor de Palabras Reservadas de C")
    print("  Lenguajes y Compiladores - UNEG  [version Python]")
    print("=" * 65)

    print("\n¿Que desea hacer?")
    print("  1) Traducir un archivo .c existente")
    print("  2) Crear archivo de prueba y traducirlo automaticamente")
    opcion = input("\nOpcion (1/2): ").strip()

    if opcion == "1":
        ruta = input("Ingrese la ruta del archivo .c: ").strip()
    elif opcion == "2":
        ruta = crear_archivo_prueba()
    else:
        print("Opcion invalida.")
        return

    # ── Paso 1: Cargar archivo en memoria dinamica ───────────────
    print(f"\n  Cargando '{ruta}' en memoria dinamica...")
    memoria = cargar_archivo_memoria(ruta)
    if memoria is None:
        return
    print(f"  OK — {len(memoria)} caracteres cargados en memoria.")

    # ── Paso 2: Crear diccionario de palabras reservadas ─────────
    print("  Creando diccionario de palabras reservadas...")
    diccionario = crear_diccionario_reservadas()
    print(f"  OK — {len(diccionario)} palabras reservadas cargadas.")

    # ── Paso 3: Tokenizar el texto ───────────────────────────────
    print("  Tokenizando el codigo fuente...")
    tokens = tokenizar(memoria)
    print(f"  OK — {len(tokens)} tokens identificados.")

    # ── Paso 4: Traducir ─────────────────────────────────────────
    print("  Traduciendo palabras reservadas...")
    tokens_traducidos, hallazgos = traducir_tokens(tokens, diccionario)
    print(f"  OK — {len(hallazgos)} palabras reservadas encontradas.")

    # ── Paso 5: Reconstruir texto ────────────────────────────────
    texto_original  = reconstruir_texto(tokens)
    texto_traducido = reconstruir_texto(tokens_traducidos)

    # ── Paso 6: Mostrar reporte ──────────────────────────────────
    mostrar_reporte(ruta, memoria, hallazgos, texto_original, texto_traducido)

    # ── Paso 7: Guardar resultado en archivo ─────────────────────
    salida = "traduccion_resultado.txt"
    with open(salida, "w", encoding="utf-8") as f:
        f.write("PALABRAS RESERVADAS ENCONTRADAS\n")
        f.write("=" * 40 + "\n")
        f.write(f"{'Linea':<8} {'Palabra C':<15} {'Traduccion'}\n")
        f.write(f"{'-'*8} {'-'*15} {'-'*20}\n")
        for h in hallazgos:
            f.write(f"{h['linea']:<8} {h['original']:<15} {h['traduccion']}\n")
        f.write("\n\nCODIGO TRADUCIDO\n")
        f.write("=" * 40 + "\n")
        f.write(texto_traducido)

    print(f"\n  Resultado guardado en '{salida}'")
    print("\n  Programa finalizado exitosamente.")


if __name__ == "__main__":
    main()
