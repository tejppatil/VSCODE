#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    char ch;
    int freq;
    struct Node *left, *right;
} Node;

Node* createNode(char ch, int freq) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->ch = ch;
    node->freq = freq;
    node->left = node->right = NULL;
    return node;
}

void swap(Node** a, Node** b) {
    Node* temp = *a;
    *a = *b;
    *b = temp;
}

void sortNodes(Node* nodes[], int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = i + 1; j < n; j++)
            if (nodes[i]->freq > nodes[j]->freq)
                swap(&nodes[i], &nodes[j]);
}

Node* buildHuffmanTree(char chars[], int freqs[], int n) {
    Node* nodes[100];
    for (int i = 0; i < n; i++)
        nodes[i] = createNode(chars[i], freqs[i]);

    int size = n;
    while (size > 1) {
        sortNodes(nodes, size);
        Node *left = nodes[0], *right = nodes[1];
        Node* merged = createNode('$', left->freq + right->freq);
        merged->left = left;
        merged->right = right;
        nodes[0] = merged;
        for (int i = 1; i < size - 1; i++)
            nodes[i] = nodes[i + 1];
        size--;
    }
    return nodes[0];
}

void printCodes(Node* root, int code[], int top) {
    if (root->left) {
        code[top] = 0;
        printCodes(root->left, code, top + 1);
    }
    if (root->right) {
        code[top] = 1;
        printCodes(root->right, code, top + 1);
    }
    if (!root->left && !root->right) {
        printf("%c: ", root->ch);
        for (int i = 0; i < top; i++)
            printf("%d", code[i]);
        printf("\n");
    }
}

int main() {
    int n;
    printf("Enter number of characters: ");
    scanf("%d", &n);

    char chars[100];
    int freqs[100];

    printf("Enter characters:\n");
    for (int i = 0; i < n; i++) {
        printf("Character %d: ", i + 1);
        scanf(" %c", &chars[i]);
    }

    printf("Enter frequencies:\n");
    for (int i = 0; i < n; i++) {
        printf("Frequency for '%c': ", chars[i]);
        scanf("%d", &freqs[i]);
    }

    Node* root = buildHuffmanTree(chars, freqs, n);

    int code[100], top = 0;
    printf("\nHuffman Codes:\n");
    printCodes(root, code, top);

    return 0;
}
