import random

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
                # Stops the path from being extended when it touches endpoint
                return valid_paths
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

def has_path_combination(all_paths: list, valid_path: list = [], index: int = 0):
    paths = all_paths[index]

    for path in paths:
        if len(set(path) & set(valid_path)) == 0:
            if index == len(all_paths) - 1:
                return True
            else:
                value = has_path_combination(all_paths, valid_path + path, index + 1)
                if value == True: return True

    return False

def is_solvable_arukone(arukone: list, pairs: int):
    all_paths = []

    for pair in range(1, pairs + 1):
        row, col = find_first_occurrence(arukone, pair)
        paths = find_path(arukone, [(pair, row, col)])
        all_paths.append(paths)

    return has_path_combination(all_paths)

def generate_arukone(field_size: int, pairs: int) -> list:
    if field_size < 5:
        raise ValueError("Parameter field_size must be greater than 4")
    
    field = [[0 for _ in range(field_size)] for _ in range(field_size)]

    for i in range(1, pairs + 1):
        index_row_a = random.randint(0, field_size - 1)
        index_item_a = random.randint(0, field_size - 1)

        index_row_b = random.randint(0, field_size - 1)
        index_item_b = random.randint(0, field_size - 1)

        if field[index_row_a][index_item_a] == 0: 
            field[index_row_a][index_item_a] = i
        if field[index_row_b][index_row_b] == 0:
            field[index_row_b][index_item_b] = i

    if not is_solvable_arukone(field, pairs):
        return generate_arukone(field_size, pairs)

    return field

print(is_solvable_arukone([
[1, 0, 2, 4, 0, 0],
[0, 0, 3, 0, 5, 0],
[0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 4],
[0, 2, 0, 0, 0, 0],
[0, 0, 0, 3, 0, 5]], 5))

# print(is_solvable_arukone([
# [1, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [2, 0, 0, 0, 0, 0, 2],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 1]], 2))

for row in generate_arukone(6, 5):
    print(row)
