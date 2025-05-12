#include <stdio.h>
#include <string.h>

int LCSLength(char X[], char Y[], int m, int n, int dp[][n+1]) {
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (X[i-1] == Y[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = (dp[i-1][j] > dp[i][j-1]) ? dp[i-1][j] : dp[i][j-1];
            }
        }
    }
    return dp[m][n];
}

void printLCS(char X[], char Y[], int m, int n, int dp[][n+1]) {
    char lcs[dp[m][n] + 1];
    int i = m, j = n, index = dp[m][n];

    lcs[index] = '\0';
    while (i > 0 && j > 0) {
        if (X[i-1] == Y[j-1]) {
            lcs[--index] = X[i-1];
            i--; j--;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            i--;
        } else {
            j--;
        }
    }

    printf("String 1: %s\n", X);
    printf("String 2: %s\n", Y);
    printf("Length of String 1: %d\n", m);
    printf("Length of String 2: %d\n", n);
    printf("Length of LCS: %d\n", dp[m][n]);
    printf("Longest Common Subsequence: %s\n", lcs);
}

int main() {
    char X[] = "ABDECGF";
    char Y[] = "ACBDFGH";
    int m = strlen(X);
    int n = strlen(Y);
    int dp[m+1][n+1];

    LCSLength(X, Y, m, n, dp);
    printLCS(X, Y, m, n, dp);
    return 0;
}
