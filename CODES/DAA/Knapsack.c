#include <stdio.h>
int max(int a, int b) {
    return (a > b) ? a : b;
}

int knapsack(int W, int weight[], int value[], int n) {
    int dp[n + 1][W + 1];

    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0)
                dp[i][w] = 0;
            else if (weight[i - 1] <= w)
                dp[i][w] = max(value[i - 1] + dp[i - 1][w - weight[i - 1]], dp[i - 1][w]);
            else
                dp[i][w] = dp[i - 1][w];
        }
    }

    int selected[n];
    for (int i = 0; i < n; i++) selected[i] = 0;

    int w = W;
    for (int i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            selected[i - 1] = 1;
            w -= weight[i - 1];
        }
    }
    printf("\nItem values: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", value[i]);
    }
    printf("\nItem weights: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", weight[i]);
    }
    printf("\nSelected item indices: ");
    for (int i = 0; i < n; i++) {
        if (selected[i])
            printf("%d ", i);
    }
    printf("\nSelected item values: ");
    for (int i = 0; i < n; i++) {
        if (selected[i])
            printf("%d ", value[i]);
    }
    printf("\nSelected item weights: ");
    for (int i = 0; i < n; i++) {
        if (selected[i])
            printf("%d ", weight[i]);
    }
    printf("\n");
    return dp[n][W];
}

int main() {
    int n, W;
    printf("Enter number of items: ");
    scanf("%d", &n);
    int value[n], weight[n];
    printf("Enter item values:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &value[i]);
    }
    printf("Enter item weights:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &weight[i]);
    }
    printf("Enter knapsack capacity: ");
    scanf("%d", &W);
    int result = knapsack(W, weight, value, n);
    printf("\nMaximum value for capacity %d is %d\n", W, result);
    return 0;
}
