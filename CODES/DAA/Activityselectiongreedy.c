#include <stdio.h>
struct Activity {
    int start;
    int finish;
};
void swap(struct Activity *a, struct Activity *b) {
    struct Activity temp = *a;
    *a = *b;
    *b = temp;
}

void sortActivities(struct Activity activities[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (activities[i].finish > activities[j].finish) {
                swap(&activities[i], &activities[j]);
            }
        }
    }
}

void activitySelection(struct Activity activities[], int n) {
    sortActivities(activities, n);
    printf("\nActivities after sorting by finish time:\n");
    for (int i = 0; i < n; i++) {
        printf("Activity %d: Start = %d, Finish = %d\n", i + 1, activities[i].start, activities[i].finish);
    }

    printf("\nSelected activities:\n");
    int lastFinish = activities[0].finish;
    printf("(%d, %d)\n", activities[0].start, activities[0].finish);
    for (int i = 1; i < n; i++) {
        if (activities[i].start >= lastFinish) {
            printf("(%d, %d)\n", activities[i].start, activities[i].finish);
            lastFinish = activities[i].finish;
        }
    }
}

int main() {
    int n;
    printf("Enter number of activities: ");
    scanf("%d", &n);
    struct Activity activities[n];
    for (int i = 0; i < n; i++) {
        printf("Enter start and finish time of activity %d:\n", i + 1);
        scanf("%d %d", &activities[i].start, &activities[i].finish);
    }
    activitySelection(activities, n);
    return 0;
}
