#include <stdio.h>
#include <sys/time.h>

int binarySearch(int array[], int startIndex, int endIndex, int x) {
    if (endIndex >= startIndex) {
        int mid = startIndex + (endIndex - startIndex) / 2;

        if (array[mid] == x)
            return mid;
        else if (array[mid] > x)
            return binarySearch(array, startIndex, mid - 1, x);
        else
            return binarySearch(array, mid + 1, endIndex, x);
    }
    return -1;
}

int main() {
    int size, ele;
    struct timeval start, end;
    printf("Enter the size of the array: ");
    scanf("%d", &size);

    int arr[size];
    printf("\nEnter elements in the array (in sorted order):\n");
    for (int i = 0; i < size; i++) {
        printf("Enter element %d: ", i);
        scanf("%d", &arr[i]);
    }

    printf("\nEnter a number to search in the array: ");
    scanf("%d", &ele);
    printf("\nPerforming Binary Search to check whether the number is in the array or not.\n");

    gettimeofday(&start, NULL);
    printf("\nTime before function call = %ld microseconds\n", start.tv_usec);

    int res = binarySearch(arr, 0, size - 1, ele);

    if (res == -1)
        printf("The number %d is not in the array.\n", ele);
    else
        printf("The number %d is present at index %d.\n", ele, res);

    gettimeofday(&end, NULL);
    printf("Time after function call = %ld microseconds\n", end.tv_usec);

    long totalTime = (end.tv_sec - start.tv_sec) * 1000000L + (end.tv_usec - start.tv_usec);
    printf("\nTotal running time = %ld microseconds\n", totalTime);

    return 0;
}
