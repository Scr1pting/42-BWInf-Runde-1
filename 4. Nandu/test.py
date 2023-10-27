import itertools

# Your array of names
names = ['Alice', 'Bob', 'Charlie']

# Generate all possible combinations of 0 and 1 for the given number of names
combinations = list(itertools.product([0, 1], repeat=len(names)))

# Create an array of dictionaries with the combinations
result = [{name: value for name, value in zip(names, combo)} for combo in combinations]

print(result)
