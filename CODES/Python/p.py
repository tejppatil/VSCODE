def sum(n):
    if n==0:
        return 0
    else:
        return n+sum(n-1)

print("The sum is ",sum(5))