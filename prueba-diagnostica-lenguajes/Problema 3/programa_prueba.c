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
        printf("factorial(%d) = %d\n", i, f);
    }

    // Verificar pares e impares
    int contador = 0;
    while (contador < n) {
        if (es_par(contador)) {
            printf("%d es par\n", contador);
        } else {
            printf("%d es impar\n", contador);
        }
        contador++;
    }

    // Uso de switch
    int dia = 3;
    switch (dia) {
        case 1:
            printf("Lunes\n");
            break;
        case 2:
            printf("Martes\n");
            break;
        case 3:
            printf("Miercoles\n");
            break;
        default:
            printf("Otro dia\n");
            break;
    }

    return 0;
}
