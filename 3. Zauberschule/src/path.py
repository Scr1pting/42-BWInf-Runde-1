import itertools


def get_surrounding_elements_3d(arr: list, level: int, row: int, col: int) -> list:
    """Determines the elements that are next to an element in a 3d list.
    Does not determine diagonally adjacent elements.

    Args:
        arr (list): 3d list
        row (int): row of list
        col (int): column of list

    Returns:
        list: contains tuples, each with level, row, column
    """
    # Initialize an empty list to store the surrounding elements
    surrounding = []

    # Determine the number of levels, rows, and columns in the 3D list
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

        # Check if the calculated level, row, and column indices are within the bounds of the list
        if 0 <= l < num_levels and 0 <= r < num_rows and 0 <= c < num_cols:
            # If the indices are valid, append a tuple containing
            # value, row index, column index of the neighboring element
            surrounding.append((l, r, c))

    return surrounding


def find_fastest_path(blueprint: list, location_a: tuple, location_b: tuple) -> list:
    """Finds the fastest path in a 3d list between location a and b.
    When a level is changed, it is counted as taking three times as long as moving on the
    same level.

    Args:
        blueprint (list): 3d list of each fields string value
        location_a (tuple): the indices of first endpoint (level, row, col)
        location_b (tuple): the indices of second endpoint (level, row, col)

    Returns:
        list: fastest path, includes "delay" elements when level is changed
    """
    # Start paths at location a
    all_paths = [[location_a]]

    iterations = 0

    while True:
        iterations += 1

        # (Re)set current paths
        current_paths = []

        # Every path is extended by one element in all possible directions
        for path in all_paths:
            # Serves to compensate when the level is changed as that takes 
            # 3 times as long as moving in one level
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

            for element in surrounding_elements:
                # If element is already in one of the paths, it doesn't make sense 
                # to add it again as there is already a faster path to that location.
                # Also prevents paths from overlapping themselves.
                # If the elements value equals "#", the path cannot be extended by that 
                if (element in already_values
                    or blueprint[element[0]][element[1]][element[2]] == "#"):
                    continue
                # Level change
                elif element[0] != last_element[0]:
                    current_paths.append(path + ["delay", "delay", element])
                else:
                    current_paths.append(path + [element])

                # If the element equals the desired endpoint, return its entire path
                # Because it was just appended to current_paths above, it is the list's last path
                if element == location_b:
                    return current_paths[-1]
        
        # If it is not possible to extend any of the existing paths, return an empty list
        if not current_paths:
            return []

        # Needed for continually expand the paths    
        all_paths = current_paths
