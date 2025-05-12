#include<iostream>
using namespace std;

int max(int a, int b) {
    return (a > b) ? a : b;
}

int extendedBottomUpCutRod(int p[], int n, int s[]) {
    int *r = new int[n + 1];
    r[0] = 0;
    for (int j = 1; j <= n; j++) {
        int q = -1;
        for (int i = 1; i <= j; i++) {
            if (q < p[i - 1] + r[j - i]) {
                q = p[i - 1] + r[j - i];
                s[j] = i;
            }
        }
        r[j] = q;
    }
    int result = r[n];
    delete[] r;
    return result;
}

void printCutRodSolution(int p[], int n) {
    int *s = new int[n + 1];
    int revenue = extendedBottomUpCutRod(p, n, s);
    cout << "Maximum Revenue: " << revenue << endl;
    cout << "Cut Rod Solution: ";
    while (n > 0) {
        cout << s[n] << " ";
        n = n - s[n];
    }
    cout << endl;
    delete[] s;
}

int main() {
    int n;
    int p[] = {1, 5, 8, 9, 10, 17, 17, 20, 24, 30};
    int length = sizeof(p) / sizeof(p[0]);
    cout << "Rod lengths and prices:" << endl;
    for (int i = 0; i < length; i++) {
        cout << "Length " << i + 1 << " : Price " << p[i] << endl;
    }
    cout << "\nEnter rod size (1 to " << length << "): ";
    cin >> n;
    if (n < 1 || n > length) {
        cout << "Invalid size" << endl;
        return 1;
    }
    printCutRodSolution(p, n);
    return 0;
}
