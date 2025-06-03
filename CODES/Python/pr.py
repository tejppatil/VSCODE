# List of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Use filter() with lambda to filter even numbers
# Both the lines are the same thing, they will return the same output
even_number = list(map(lambda x: x % 2 == 0, numbers))
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
# even_numbers = list(filter(lambda x: True if x % 2 == 0 else False, numbers))

print(even_number)
print(even_numbers)