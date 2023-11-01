import itertools


def get_surrounding_elements_3d(arr: list, level: int, row: int, col: int) -> list:
    """Determines the elements that are next to an element in a 3d array.
    Does not determine diagonally adjacent elements.

    Args:
        arr (list): 3d array
        row (int): row of array
        col (int): column of array

    Returns:
        list: contains tuples, each with level, row, column
    """
    # Initialize an empty list to store the surrounding elements
    surrounding = []

    # Determine the number of levels, rows, and columns in the 3D array
    num_levels = len(arr)
    num_rows = len(arr[0])
    num_cols = len(arr[0][0])

    # Define the relative positions of the surrounding elements
    positions = [
        (-1, 0, 0), (1, 0, 0), # Above & below
        (0, -1, 0), (0, 1, 0), # Up & down
        (0, 0, -1), (0, 0, 1)  # Left & right
    ]

    # Iterate through each relative position to check for neighboring elements
    for level_offset, row_offset, col_offset in positions:
        l = level + level_offset
        r = row + row_offset  # Calculate the row index of the neighboring element
        c = col + col_offset  # Calculate the column index of the neighboring element

        # Check if the calculated level, row, and column indices are within the bounds of the array
        if 0 <= l < num_levels and 0 <= r < num_rows and 0 <= c < num_cols:
            # If the indices are valid, append a tuple containing
            # value, row index, column index of the neighboring element
            surrounding.append((l, r, c))

    return surrounding


def find_fastest_path(blueprint: list, location_a: tuple, location_b: tuple) -> list:
    all_paths = [[location_a]]

    iterations = 0

    while True:
        if not all_paths:
            return []

        iterations += 1
        current_paths = []

        for path in all_paths:
            if len(path) > iterations:
                current_paths.append(path)
                continue

            last_element = path[-1]

            surrounding_elements = get_surrounding_elements_3d(
                arr=blueprint,
                level=last_element[0],
                row=last_element[1],
                col=last_element[2]
            )

            already_values = list(itertools.chain.from_iterable(all_paths + current_paths))
            possible_elements = []

            for element in surrounding_elements:
                if (element in path 
                    or element in already_values
                    or blueprint[element[0]][element[1]][element[2]] == "#"):
                    continue
                elif element[0] != last_element[0]:
                    current_paths.append(path + ["delay", "delay", element])
                else:
                    current_paths.append(path + [element])

                possible_elements.append(element)

                if element == location_b:
                    return current_paths[-1]
                
        all_paths = current_paths
