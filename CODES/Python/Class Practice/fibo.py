size = int(input("Enter size: "))

fibonacci = lambda n: n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

for i in range(size):
    print(fibonacci(i), end = ", " if i < size - 1 else "")
