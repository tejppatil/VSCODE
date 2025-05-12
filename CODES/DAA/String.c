#include <stdio.h>
#include <string.h>

void stringconcatenation(char a[], char b[]) {
    int len1 = strlen(a);
    int len2 = strlen(b);
    char c[len1 + len2 + 1];  

    int i, j;
    for (i = 0; a[i] != '\0'; i++) {
        c[i] = a[i];
    }
    for (j = 0; b[j] != '\0'; j++) {
        c[i + j] = b[j];
    }
    c[i + j] = '\0';  

    printf("Concatenated String: %s\n", c);
}

void stringlength(char a[], char b[], int *s1length, int *s2length) {
    *s1length = strlen(a);
    *s2length = strlen(b);
}

void stringcompare(char a[], char b[]) {
    if (strcmp(a, b) == 0) {
        printf("Strings are Equal\n");
    } else {
        printf("Strings are Not Equal\n");
    }
}

int main() {
    int n, len1, len2;
    char s1[50], s2[50];

    printf("Enter first string: ");
    fgets(s1, sizeof(s1), stdin);
    s1[strcspn(s1, "\n")] = '\0';  

    printf("Enter second string: ");
    fgets(s2, sizeof(s2), stdin);
    s2[strcspn(s2, "\n")] = '\0';  


    while(1){
        printf("Press\n1:String Concatenation\n2:String Length\n3:String Comparison\n4:Exit\nEnter here:");
        scanf("%d",&n);
        switch(n){
            case 1:
            stringconcatenation(s1, s2);
            break;
            
            case 2:
            stringlength(s1, s2, &len1, &len2);
            printf("Length of first string: %d\n", len1);
            printf("Length of second string: %d\n", len2);
            break;

            case 3:
            stringcompare(s1, s2);
            break;

            case 4:
            return 0;

            default:
            printf("Invalid Choice:::Enter value Correctly");
            break;
        }
    }
    return 0;
}
