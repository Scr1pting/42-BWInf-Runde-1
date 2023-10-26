import random

def generate_arukone(field_size: int, pairs: int) -> list:
    if field_size < 5:
        raise ValueError("Parameter field_size must be greater than 4")
    
    field = [[0 for _ in range(field_size)] for _ in range(field_size)]

    for i in range(0, pairs):
        index_row_a = random.randint(0, field_size - 1)
        index_item_a = random.randint(0, field_size - 1)

        index_row_b = random.randint(0, field_size - 1)
        index_item_b = random.randint(0, field_size - 1)

        if field[index_row_a][index_item_a] == 0: 
            field[index_row_a][index_item_a] = i + 1
        if field[index_row_b][index_row_b] == 0:
            field[index_row_b][index_item_b] = i + 1

    return field

def find_first_occurrence(arr, target):
        for row_index, row in enumerate(arr):
            for col_index, value in enumerate(row):
                if value == target:
                    return (row_index, col_index)  # Return the indices of the first occurrence

        return None  # Return None if the element is not found in the array

def get_surrounding_elements(arr, row: int, col: int) -> tuple:
    surrounding = []
    num_rows = len(arr)
    num_cols = len(arr[0])

    # Define the relative positions of the surrounding elements
    positions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    for row_offset, col_offset in positions:
        r = row + row_offset
        c = col + col_offset

        if 0 <= r < num_rows and 0 <= c < num_cols:
            surrounding.append((arr[r][c], r, c))

    return surrounding

def find_path(arukone: list, original_path: list) -> tuple:
    _, row, col = original_path[-1]

    surrounding_elements = get_surrounding_elements(arukone, row, col)
    
    paths = []
    valid_paths = []

    # Detect whether path touches itself
    if len(set(original_path) & set(surrounding_elements)) > 1:
        return []
    
    for element in surrounding_elements:
        value = element[0]
        
        if element not in original_path:
            if value == original_path[0][0]:
                valid_paths.append(original_path + [element])
            elif value == 0:
                paths.append(original_path + [element])

    for path in paths:
        valid_paths += find_path(arukone, path)

    return valid_paths

def find_first_occurrence(arr, target):
        for row_index, row in enumerate(arr):
            for col_index, value in enumerate(row):
                if value == target:
                    return (row_index, col_index)  # Return the indices of the first occurrence

        return None  # Return None if the element is not found in the array

def solve_arukone(arukone: list, pairs: int):
    all_paths = []

    for pair in pairs:
        paths = find_first_occurrence(arukone, pair + 1)
        all_paths.append(paths)


paths = find_path([
[1, 0, 2, 4, 0, 0],
[0, 0, 3, 0, 5, 0],
[0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 4],
[0, 2, 0, 0, 0, 0],
[0, 0, 0, 3, 0, 5]], [(1, 0, 0)])

for path in paths:
    print(path)
