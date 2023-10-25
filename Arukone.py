import math
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

def get_surrounding_elements(arr, row: int, col: int) -> tuple:

    surrounding = []
    num_rows = len(arr)
    num_cols = len(arr[0])

    # Define the relative positions of the surrounding elements
    positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for row_offset, col_offset in positions:
        r = row + row_offset
        c = col + col_offset

        if 0 <= r < num_rows and 0 <= c < num_cols:
            surrounding.append((arr[r][c], r, c))

    return surrounding

def find_path(arukone: list, path: list) -> tuple:
    row, col = path[-1]

    elements = get_surrounding_elements(arukone, row, col)

    paths = []
    all_paths = []

    for element in elements:
        value, element_row, element_col = element
        
        if value == 0 and (element_row, element_col) not in path:
            paths.append(path + [(element_row, element_col)])

    for path in paths:
        all_paths = find_path(arukone, path)
        print(find_path(arukone, path))

    return all_paths


print(find_path([
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 2, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 2, 0, 0]], [(2, 4)]))
