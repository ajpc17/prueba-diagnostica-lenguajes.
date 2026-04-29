/*
 * Problema 1 - Triangulo de Pascal y Evaluacion de Polinomio (x+1)^n
 * Curso: Lenguajes y Compiladores - UNEG
 * Implementacion: C con memoria dinamica real (malloc / free)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

/* ===========================================================
 *  FUNCION: generar_coeficientes
 *  Recibe : n (grado del polinomio)
 *  Retorna: puntero a arreglo dinamico con n+1 coeficientes
 *           El llamador es responsable de liberar la memoria
 * ===========================================================
 *
 *  MEMORIA DINAMICA:
 *  En cada fila del triangulo pedimos al sistema operativo
 *  exactamente la memoria que necesitamos con malloc().
 *  La fila anterior se libera con free() una vez que ya
 *  no la necesitamos, evitando fugas de memoria.
 *
 *  Representacion interna:
 *
 *  fila_anterior -> [ 1 ]                    (n=0)
 *  fila_actual   -> [ 1 | 1 ]                (n=1)
 *  fila_actual   -> [ 1 | 2 | 1 ]            (n=2)
 *  fila_actual   -> [ 1 | 3 | 3 | 1 ]        (n=3)
 *                      ^               ^
 *                   malloc()        free() al terminar
 */
long long* generar_coeficientes(int n) {

    /* Caso base: (x+1)^0 = 1 */
    if (n == 0) {
        long long* base = (long long*) malloc(sizeof(long long));
        if (!base) { fprintf(stderr, "Error: malloc fallo\n"); exit(1); }
        base[0] = 1;
        return base;
    }

    /* Empezamos con la fila 0 del triangulo: [1] */
    long long* fila_anterior = (long long*) malloc(sizeof(long long));
    if (!fila_anterior) { fprintf(stderr, "Error: malloc fallo\n"); exit(1); }
    fila_anterior[0] = 1;

    long long* fila_actual = NULL;

    for (int i = 1; i <= n; i++) {

        /* Pedimos memoria para i+1 elementos (la fila i tiene i+1 numeros) */
        fila_actual = (long long*) malloc((i + 1) * sizeof(long long));
        if (!fila_actual) { fprintf(stderr, "Error: malloc fallo\n"); exit(1); }

        /* Primer y ultimo elemento de cada fila siempre son 1 */
        fila_actual[0] = 1;
        fila_actual[i] = 1;

        /* Los elementos del medio: suma de los dos de arriba */
        for (int j = 1; j < i; j++) {
            fila_actual[j] = fila_anterior[j - 1] + fila_anterior[j];
        }

        /* Ya no necesitamos la fila anterior: liberamos su memoria */
        free(fila_anterior);

        /* La fila actual se convierte en la anterior para la proxima iteracion */
        fila_anterior = fila_actual;
    }

    return fila_actual;  /* Devolvemos el puntero, el llamador hara free() */
}


/* ===========================================================
 *  FUNCION: mostrar_polinomio
 *  Imprime en pantalla la expresion algebraica del polinomio
 *  Ejemplo: [1,3,3,1] con n=3 -> "x^3 + 3x^2 + 3x + 1"
 * =========================================================== */
void mostrar_polinomio(long long* coef, int n) {
    int primero = 1;  /* Bandera para no imprimir "+" antes del primer termino */

    for (int i = 0; i <= n; i++) {
        int exponente = n - i;
        long long c = coef[i];

        if (c == 0) continue;

        /* Separador entre terminos */
        if (!primero) printf(" + ");
        primero = 0;

        if (exponente == 0) {
            /* Termino independiente: solo el numero */
            printf("%lld", c);
        } else if (exponente == 1) {
            /* Termino lineal */
            if (c == 1) printf("x");
            else        printf("%lldx", c);
        } else {
            /* Termino con potencia */
            if (c == 1) printf("x^%d", exponente);
            else        printf("%lldx^%d", c, exponente);
        }
    }
    printf("\n");
}


/* ===========================================================
 *  FUNCION: potencia_entera
 *  Calcula base^exp de forma iterativa (sin usar pow())
 *  para trabajar con enteros exactos
 * =========================================================== */
double potencia(double base, int exp) {
    double resultado = 1.0;
    for (int i = 0; i < exp; i++) resultado *= base;
    return resultado;
}

int es_entero(double valor) {
    long long entero = (long long) valor;
    return fabs(valor - entero) < 1e-9;
}

void imprimir_numero(double valor) {
    if (es_entero(valor))
        printf("%lld", (long long) valor);
    else
        printf("%.4f", valor);
}


/* ===========================================================
 *  FUNCION: evaluar_polinomio_pasos
 *  Evalua f(x) termino a termino mostrando cada paso
 * =========================================================== */
double evaluar_polinomio_pasos(long long* coef, int n, double x) {
    printf("\n=======================================================\n");
    printf("  Evaluacion paso a paso de f(");
    imprimir_numero(x);
    printf(") = (x+1)^%d\n", n);
    printf("=======================================================\n");

    if (n == 0) {
        printf("  f(");
        imprimir_numero(x);
        printf(") = 1\n");
        return 1.0;
    }

    printf("\n  Sustituyendo x = ");
    imprimir_numero(x);
    printf(":\n\n");

    double resultado = 0.0;

    for (int i = 0; i <= n; i++) {
        int exp      = n - i;
        double xpow  = potencia(x, exp);
        double valor = coef[i] * xpow;
        resultado   += valor;

        if (exp == 0) {
            printf("    Termino %2d: %lld x^0 = %lld x 1 = ", i+1, coef[i], coef[i]);
            imprimir_numero(valor);
            printf("\n");
        } else if (exp == 1) {
            printf("    Termino %2d: %lld x^1 = %lld x ", i+1, coef[i], coef[i]);
            imprimir_numero(x);
            printf(" = ");
            imprimir_numero(valor);
            printf("\n");
        } else {
            printf("    Termino %2d: %lld x^%d = %lld x ", i+1, coef[i], exp, coef[i]);
            imprimir_numero(xpow);
            printf(" = ");
            imprimir_numero(valor);
            printf("\n");
        }
    }

    printf("\n  Resultado f(");
    imprimir_numero(x);
    printf(") = ");
    imprimir_numero(resultado);
    printf("\n");
    printf("  Verificacion directa: (");
    imprimir_numero(x);
    printf("+1)^%d = ", n);
    imprimir_numero(potencia(x + 1, n));
    printf("\n");
    printf("=======================================================\n");

    return resultado;
}


/* ===========================================================
 *  FUNCION: medir_y_guardar_n100
 *  Mide el tiempo para n=100 y escribe los resultados en
 *  un archivo .txt junto con el tiempo de Python para comparar
 * =========================================================== */
void medir_y_guardar_n100(double tiempo_python_ms) {
    int n = 100;

    /* --- Medicion de tiempo con clock() --- */
    clock_t inicio = clock();

    long long* coef = generar_coeficientes(n);

    clock_t fin = clock();

    double tiempo_ms = (double)(fin - inicio) / CLOCKS_PER_SEC * 1000.0;

    printf("\n=======================================================\n");
    printf("  MEDICION DE TIEMPO PARA n=%d\n", n);
    printf("=======================================================\n");
    printf("  Tiempo C      : %.6f ms\n", tiempo_ms);
    printf("  Tiempo Python : %.6f ms\n", tiempo_python_ms);
    if (tiempo_python_ms > 0)
        printf("  C es %.1fx mas rapido que Python\n",
               tiempo_python_ms / tiempo_ms);
    printf("  Coeficientes generados: %d\n", n + 1);

    /* --- Escritura en archivo TXT --- */
    FILE* archivo = fopen("resultado_n100.txt", "a");  /* append: agrega al existente */
    if (!archivo) {
        fprintf(stderr, "Error: no se pudo abrir resultado_n100.txt\n");
        free(coef);
        return;
    }

    fprintf(archivo, "\n");
    fprintf(archivo, "========================================\n");
    fprintf(archivo, "RESULTADO EN C para n=%d\n", n);
    fprintf(archivo, "========================================\n");
    fprintf(archivo, "Tiempo de ejecucion C      : %.6f ms\n", tiempo_ms);
    fprintf(archivo, "Tiempo de ejecucion Python : %.6f ms\n", tiempo_python_ms);
    if (tiempo_python_ms > 0)
        fprintf(archivo, "C es %.1fx mas rapido que Python\n",
                tiempo_python_ms / tiempo_ms);
    fprintf(archivo, "\nCoeficientes de (x+1)^%d:\n", n);
    for (int i = 0; i <= n; i++) {
        fprintf(archivo, "  C(%3d) = %lld\n", i, coef[i]);
    }
    fclose(archivo);

    printf("  Resultados agregados en 'resultado_n100.txt'\n");
    printf("=======================================================\n");

    free(coef);  /* IMPORTANTE: liberamos la memoria pedida con malloc() */
}


/* ===========================================================
 *  FUNCION PRINCIPAL
 * =========================================================== */
int main() {
    printf("=======================================================\n");
    printf("  PROBLEMA 1: Triangulo de Pascal - (x+1)^n\n");
    printf("  Lenguajes y Compiladores - UNEG  [version C]\n");
    printf("=======================================================\n");

    /* --- Parte a): Pedir n y generar coeficientes --- */
    int n;
    printf("\nIngrese el valor de n (entero no negativo): ");
    if (scanf("%d", &n) != 1 || n < 0) {
        fprintf(stderr, "Error: n debe ser un entero no negativo.\n");
        return 1;
    }

    printf("\n  Generando coeficientes para (x+1)^%d...\n\n", n);

    /* Llamada con memoria dinamica */
    long long* coeficientes = generar_coeficientes(n);

    /* Mostrar la fila del triangulo */
    printf("  Coeficientes (fila %d del Triangulo de Pascal):\n  [ ", n);
    for (int i = 0; i <= n; i++) {
        printf("%lld", coeficientes[i]);
        if (i < n) printf(", ");
    }
    printf(" ]\n");

    /* Mostrar el polinomio */
    printf("\n  Polinomio resultante:\n");
    printf("  f(x) = (x+1)^%d = ", n);
    mostrar_polinomio(coeficientes, n);

    /* --- Parte b): Evaluar para x dado --- */
    double x;
    printf("\nIngrese el valor de x para evaluar f(x) = (x+1)^%d: ", n);
    if (scanf("%lf", &x) != 1) {
        fprintf(stderr, "Error: ingrese un numero valido.\n");
        free(coeficientes);
        return 1;
    }

    evaluar_polinomio_pasos(coeficientes, n, x);

    /* Liberamos la memoria de los coeficientes del polinomio */
    free(coeficientes);

    /* --- Medicion n=100 y comparacion con Python --- */
    double tiempo_python = 0.261558;  /* Tiempo medido previamente en Python */
    medir_y_guardar_n100(tiempo_python);

    printf("\n¡Programa finalizado exitosamente!\n\n");
    return 0;
}
