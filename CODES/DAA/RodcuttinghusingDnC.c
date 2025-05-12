#include <stdio.h>
#include <time.h>

int max(int a, int b) {
    return (a > b) ? a : b;
}

int cutRod(int p[], int n) {
    if (n == 0)
        return 0;
    int q = 0;
    for (int i = 1; i <= n; i++) {
        q = max(q, p[i - 1] + cutRod(p, n - i));
    }
    return q;
}

int main() {
    int n;
    int p[] = {1, 5, 8, 9, 10, 17, 17, 20, 24, 30};
    int length = sizeof(p) / sizeof(p[0]);

    printf("Rod lengths and prices:\n");
    for (int i = 0; i < length; i++) {
        printf("Length %2d : Price %2d\n", i + 1, p[i]);
    }

    printf("\nEnter rod size (1 to %d): ", length);
    scanf("%d", &n);

    if (n < 1 || n > length) {
        printf("Invalid size\n");
        return 1;
    }

    clock_t t = clock();
    int result = cutRod(p, n);
    t = clock() - t;
    double time_taken = ((double)t) / CLOCKS_PER_SEC;

    printf("Maximum price: %d\n", result);
    printf("Execution time: %f seconds\n", time_taken);

    return 0;
}
