#include <stdio.h>
#include <stdlib.h>
struct Item {
    int value;
    int weight;
    float ratio;
};

int compare(const void *a, const void *b) {
    float r1 = ((struct Item *)a)->ratio;
    float r2 = ((struct Item *)b)->ratio;
    return (r2 > r1) - (r2 < r1);
}

int main() {
    int n;
    float capacity;
    printf("Enter number of items: ");
    scanf("%d", &n);
    struct Item items[n];
    printf("Enter the values of the items:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &items[i].value);
    }
    printf("Enter the weights of the items:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &items[i].weight);
        items[i].ratio = (float)items[i].value / items[i].weight;
    }
    printf("Enter the capacity of the knapsack: ");
    scanf("%f", &capacity);
    qsort(items, n, sizeof(struct Item), compare);
    float total_value = 0.0;
    float total_weight = 0.0;

    printf("\nSelected items (value, weight, fraction):\n");
    for (int i = 0; i < n && capacity > 0; i++) {
        if (items[i].weight <= capacity) {
            capacity -= items[i].weight;
            total_value += items[i].value;
            total_weight += items[i].weight;
            printf("(%d, %d, 1.00)\n", items[i].value, items[i].weight);
        } else {
            float fraction = capacity / items[i].weight;
            total_value += items[i].value * fraction;
            total_weight += items[i].weight * fraction;
            printf("(%d, %d, %.2f)\n", items[i].value, items[i].weight, fraction);
            capacity = 0;
        }
    }
    printf("\nTotal weight used: %.2f\n", total_weight);
    printf("Maximum value in knapsack = %.2f\n", total_value);
    return 0;
}
