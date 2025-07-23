def list(l,idx):
    if (idx == len(l)):
        return
    print(l[idx])
    list(l,idx+1)

fruits = ["m", "r", "a"]
list(fruits, 0)