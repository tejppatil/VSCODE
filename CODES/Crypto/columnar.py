def encrypt(text, key):
    text = text.replace(" ", "")
    cols = len(key)
    matrix = build_matrix(text, cols)
    print_matrix(matrix, key)
    
    order = get_order(key)
    cipher = ""

    for num in range(1, cols + 1):
        col = order.index(num)
        for row in matrix:
            if col < len(row):
                cipher += row[col]

    return cipher

def build_matrix(text, width):
    matrix = []
    for i in range(0, len(text), width):
        matrix.append(list(text[i:i+width]))
    return matrix

def print_matrix(matrix, key):
    print("\nMatrix:")
    print("Key:   ", " ".join(key))
    for row in matrix:
        print("       ", " ".join(row))

def get_order(key):
    order = []
    for i, ch in enumerate(key):
        count = 1
        for j in range(i):
            if key[j] <= ch:
                count += 1
            else:
                order[j] += 1
        order.append(count)
    return order

text = input("Enter the plaintext: ")
key = input("Enter the keyword: ")
result = encrypt(text, key)
print("The Encrypted Text:", result)
