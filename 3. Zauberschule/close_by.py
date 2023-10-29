def get_valid_descents(map_top: list, map_bottom: list) -> list:
    get_valid_descents = []

    for row_index, row in enumerate(map_top):
        for col_index, value in enumerate(row):
            if value == 1 and map_bottom[row_index][col_index] == 1:
                get_valid_descents.append((row_index, col_index))
    
    return get_valid_descents
